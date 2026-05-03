from discord.ext import commands
from utils.play_utils import PlayUtils

class PlayerCog(commands.Cog):
    """Music playback commands: play, queue, skip, pause, resume, stop."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.play_utils = PlayUtils()

    @commands.hybrid_command(name="play", description="Spielt einen Song ab und fügt ihn der Queue hinzu.")
    async def play(self, ctx: commands.Context, *, link: str):
        if not link or not link.strip():
            return await ctx.send("Link fehlt.", ephemeral=True)
        if not getattr(ctx.author, 'voice', None) or not ctx.author.voice.channel:
            return await ctx.send("Du musst in einem Sprachkanal sein!", ephemeral=True)
        await ctx.defer()
        await self.play_utils.add_to_queue(ctx, link)
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await self.play_utils.play_next(ctx)

    @commands.hybrid_command(name="queue", description="Zeigt die aktuelle Queue an.")
    async def queue(self, ctx: commands.Context):
        await ctx.defer()
        queue = self.play_utils.get_queue(ctx.guild.id) if ctx.guild else []
        current = self.play_utils.current_song.get(ctx.guild.id)
        lines = []
        if current:
            lines.append("**Now Playing:**")
            lines.append(f"▶️ {current[0]} ([Link](<{current[1]}>))")
            lines.append("")
        if queue:
            lines.append("**Up Next:**")
            for i, itm in enumerate(queue[:5], 1):
                if isinstance(itm, dict):
                    tracks = itm.get('tracks', [])
                    idx = itm.get('current_index', 0)
                    for j, (t, a) in enumerate(tracks[idx:idx+5], idx+1):
                        link = self.play_utils._bridge_to_youtube(f"{t} {a}") or "#"
                        lines.append(f"{j}. {t} - {a} ([Link](<{link}>))")
                else:
                    lines.append(f"{i}. {itm[0]} ([Link](<{itm[1]}>))")
        if not lines:
            return await ctx.send("Die Warteschlange ist leer.")
        await ctx.send("\n".join(lines)[:2000])

    @commands.hybrid_command(name="skip", description="Überspringt den aktuellen Song oder mehrere Tracks.")
    async def skip(self, ctx: commands.Context, amount: int = 1):
        if amount < 1:
            return await self.play_utils.safe_send(ctx, "Mindestwert ist 1.")
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await self.play_utils.safe_send(ctx, "Nichts läuft gerade.")
        await ctx.defer()
        if amount == 1:
            q = self.play_utils.get_queue(ctx.guild.id)
            next_title = None
            if q:
                itm = q[0]
                if isinstance(itm, dict):
                    peek = await self.play_utils._get_next_spotify_track(itm, ctx)
                    next_title = peek[0] if peek else None
                else:
                    next_title = itm[0]
            ctx.voice_client.stop()
            msg = f"Weiter: **{next_title}**" if next_title else "Keine nächsten Songs."
            return await self.play_utils.safe_send(ctx, msg)
        skipped = await self.play_utils.skip_tracks(ctx, amount)
        ctx.voice_client.stop()
        q = self.play_utils.get_queue(ctx.guild.id)
        next_title = None
        if q:
            itm = q[0]
            if isinstance(itm, dict):
                peek = await self.play_utils._get_next_spotify_track(itm, ctx)
                next_title = peek[0] if peek else None
            else:
                next_title = itm[0]
        msg = (f"{amount} übersprungen, weiter: **{next_title}**" if next_title
               else f"{amount} übersprungen, keine nächsten Songs")
        return await self.play_utils.safe_send(ctx, msg)

    @commands.hybrid_command(name="clear_queue", description="Leert die aktuelle Warteschlange.")
    async def clear_queue(self, ctx: commands.Context):
        return await self.play_utils.clear_queue(ctx)

    @commands.hybrid_command(name="pause", description="Pausiert die Wiedergabe.")
    async def pause(self, ctx: commands.Context):
        await self.play_utils.pause(ctx)
        await ctx.send("Pausiert.")

    @commands.hybrid_command(name="resume", description="Setzt die Wiedergabe fort.")
    async def resume(self, ctx: commands.Context):
        await self.play_utils.resume(ctx)
        await ctx.send("Fortgesetzt.")

    @commands.hybrid_command(name="stop", description="Stoppt die Wiedergabe und verlässt den Sprachkanal.")
    async def stop(self, ctx: commands.Context):
        await self.play_utils.stop(ctx)
        await ctx.send("Gestoppt und Kanal verlassen.")

async def setup(client: commands.Bot):
    await client.add_cog(PlayerCog(client))

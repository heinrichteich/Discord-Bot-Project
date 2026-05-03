import discord
import io
from discord.ext import commands
from utils.check_utils import check_image_async

class CheckCog(commands.Cog):
    """Image analysis commands (/check)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.memory = {}

    @commands.hybrid_command(name='check', description='Prüft Bild anhand Prompt')
    async def check(self, ctx: commands.Context, file: discord.Attachment, *, prompt: str):
        allowed = ('.png', '.jpg', '.jpeg', '.bmp')
        if not file.filename.lower().endswith(allowed):
            return await ctx.send('Invalid file type.', ephemeral=False)
        await ctx.defer()
        try:
            img_bytes = await file.read()
        except Exception as e:
            return await ctx.send(f'Error reading file: {e}')
        try:
            result = await check_image_async(img_bytes, prompt)
        except Exception as e:
            return await ctx.send(f'Check failed: {e}')
        self.memory[ctx.channel.id] = {
            'image': img_bytes,
            'result': result,
            'prompt': prompt
        }
        embed = discord.Embed(title='Check Result', description=result, color=discord.Color.blue())
        embed.set_footer(text='Original image attached below.')
        discord_file = discord.File(io.BytesIO(img_bytes), filename=file.filename)
        embed.set_image(url=f'attachment://{file.filename}')
        await ctx.send(embed=embed, file=discord_file)

async def setup(bot: commands.Bot):
    await bot.add_cog(CheckCog(bot))

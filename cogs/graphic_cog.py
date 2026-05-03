import io
import discord
import os
import aiohttp
from discord.ext import commands
from typing import Literal
from utils.graphic_utils import GraphicUtils
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

graphic_utils = GraphicUtils()

class GraphicCog(commands.Cog):
    """Image and video processing commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    '''@commands.hybrid_command(
        name='image',
        description='Generiert ein Bild mit DALL·E 3 (Standard, 1024×1024).'
    )
    async def image(self, ctx: commands.Context, prompt: str):
        await ctx.defer()
        try:
            resp = client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                quality='standard',
                n=1,
                size='1024x1024'
            )
            image_url = resp.data[0].url
        except Exception as e:
            return await ctx.send(f'Error generating image: {e}')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as r:
                    if r.status != 200:
                        return await ctx.send(f'Error downloading image: HTTP {r.status}')
                    img_data = await r.read()
        except Exception as e:
            return await ctx.send(f'Error downloading image: {e}')
        filename = 'generated_image.png'
        file = discord.File(io.BytesIO(img_data), filename=filename)
        embed = discord.Embed()
        embed.set_image(url=f'attachment://{filename}')
        embed.set_footer(text=f'Generated with prompt: {prompt}')
        await ctx.send(file=file, embed=embed)'''

    @commands.hybrid_command(name='sw', description='Konvertiert Medien in Schwarz-Weiß')
    async def sw(self, ctx: commands.Context, input_file: discord.Attachment):
        await ctx.defer()
        try:
            data = await input_file.read()
        except Exception as e:
            return await ctx.send(f'Error downloading file: {e}')
        name = input_file.filename.lower()
        if name.endswith(('.png', '.jpg', '.bmp', '.jpeg')):
            result = graphic_utils.convert_to_grayscale_image(data)
            out_name = 'sw_result.png'
        elif name.endswith(('.mp4', '.avi')):
            result = graphic_utils.convert_to_grayscale_video(data)
            out_name = 'sw_result.mp4'
        else:
            return await ctx.send('Invalid file format.')
        buf = io.BytesIO(result)
        buf.seek(0)
        await ctx.send(file=discord.File(buf, filename=out_name))

    @commands.hybrid_command(name='watermark', description='Wasserzeichen auf Bild oder Video anwenden')
    async def watermark(self, ctx: commands.Context, input_file: discord.Attachment, watermark_file: discord.Attachment,
                        position: Literal['top-left','top-right','bottom-left','bottom-right','center']='center',
                        scale: str='1.0', transparency: str='1.0'):
        await ctx.defer()
        try:
            data_in = await input_file.read()
            data_wm = await watermark_file.read()
        except Exception as e:
            return await ctx.send(f'Error downloading files: {e}')
        def parse_decimal(val: str) -> float:
            try:
                return float(val)
            except ValueError:
                return float(val.replace(',', '.'))
        try:
            sc = parse_decimal(scale)
            tr = parse_decimal(transparency)
        except Exception:
            return await ctx.send('Invalid number format.')
        name = input_file.filename.lower()
        if name.endswith(('.png', '.jpg', '.bmp', '.jpeg')):
            out = graphic_utils.watermark_image_file(data_in, data_wm, position, sc, tr)
            out_name = 'watermark_result.png'
        elif name.endswith(('.mp4', '.mov')):
            out = graphic_utils.watermark_video_file(data_in, data_wm, position, sc, tr)
            out_name = 'watermark_result.mp4'
        else:
            return await ctx.send('Invalid file format.')
        buf2 = io.BytesIO(out)
        buf2.seek(0)
        await ctx.send(file=discord.File(buf2, filename=out_name))

async def setup(bot: commands.Bot):
    await bot.add_cog(GraphicCog(bot))

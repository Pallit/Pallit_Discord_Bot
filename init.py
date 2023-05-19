import asyncio

import discord
from discord.ext import commands
import requests
import validators
from urllib.parse import urlparse
import youtube_dl

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


links = []

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command(name='add')
async def add(ctx, arg):

    if not validators.url(str(arg)):
        await ctx.channel.send('Необходимо ввести ссылку на видео после команды !add')
        return
    else:
        r = requests.get(str(arg))
        if r.status_code != 200:
            await ctx.channel.send('404 error')
            return
        domain = urlparse(str(arg)).netloc
        if domain != 'www.youtube.com':
            await ctx.channel.send('Необходимо ввести ссылку на видео из youtube.com')
            return
        links.append(str(arg))
        await ctx.channel.send('Добавлено!')


@bot.command(name='list')
async def links_list(ctx):
    await ctx.channel.send(links)


@bot.command(name='play')
async def play(ctx):
    if not ctx.message.author.voice:
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.event
async def on_voice_state_update(member, before, after):
    bot_client = discord.utils.get(bot.voice_clients)
    if before.channel is None:
        return
    if bot_client is None:
        return
    if len(before.channel.members) == 1 and bot_client.is_connected():
        await bot_client.disconnect(force=True)


bot.run('MTEwOTE3NjEzMzI2Nzc3MTU4Mw.GbVN6d.cTgxwHDUaekXvU7CRc9UrfE-6Lg-FgjclO4y1w')

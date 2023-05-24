import discord
from discord.ext import commands
import requests
import validators
from urllib.parse import urlparse
import yt_dlp

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


links = []

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
async def play(ctx, url):
    if not ctx.message.author.voice:
        return
    else:
        channel = ctx.message.author.voice.channel
    bot_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if bot_client is None:
        await channel.connect()

    server = ctx.message.guild
    channel = server.voice_client
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')


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

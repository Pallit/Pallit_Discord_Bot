import discord
from discord.ext import commands
import requests
import validators
from urllib.parse import urlparse
import yt_dlp
import asyncio
from youtubesearchpython import VideosSearch
import os


bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

links = []


@bot.command(name='add')
async def add(ctx, arg):
    if not validators.url(str(arg)):
        videos_search = VideosSearch(str(arg), limit=1)
        link = videos_search.result()['result'][0]['link']
        links.append(link)
        await ctx.channel.send('добавлено: '+link)
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
        await ctx.channel.send('добавлено')


@bot.command(name='list')
async def links_list(ctx):
    if len(links) > 0:
        await ctx.channel.send(links)
    else:
        await ctx.channel.send('Очередь пуста')


@bot.command(name='clear')
async def clear_links_list(ctx):
    links.clear()
    await ctx.channel.send('Очередь очищена')


@bot.command(name='play')
async def play(ctx):
    if len(links) == 0:
        await ctx.channel.send('Очередь пуста')
        return
    if not ctx.message.author.voice:
        return
    channel = ctx.message.author.voice.channel
    bot_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if bot_client is None:
        await channel.connect()

    YDL_OPTIONS = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing() and len(links) > 0:
        url = links.pop(0)
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(source=discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            await ctx.channel.send('Сейчас играет: ' + url)
        except yt_dlp.utils.DownloadError:
            await ctx.channel.send('Видео недоступно: ' + url)
            await play(ctx)


def play_next(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if len(links) > 0 and not voice.is_playing():
        asyncio.run_coroutine_threadsafe(play(ctx), bot.loop)


@bot.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await voice.disconnect(force=True)


@bot.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()


@bot.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()


@bot.command(name='skip')
async def skip(ctx):
    await stop(ctx)
    await play(ctx)


@bot.event
async def on_voice_state_update(member, before, after):
    bot_client = discord.utils.get(bot.voice_clients)
    if before.channel is None:
        return
    if bot_client is None:
        return
    if len(before.channel.members) == 1 and bot_client.is_connected():
        await bot_client.disconnect(force=True)


try:
    token = os.environ['R_TELEGRAM_BOT_botname']
    bot.run(token)
except KeyError:
    print("Токен не найден")

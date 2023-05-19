import discord
from discord.ext import commands
import requests
import validators
from urllib.parse import urlparse

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



bot.run('MTA5NDcwMzYyODMxNDQ5Mjk2OA.Gzgt1e.NCWYC9g5zeicubJz8SZE2FIGsoSoSdhPw5xRIw')

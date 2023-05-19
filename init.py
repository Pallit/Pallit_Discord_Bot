import discord
from discord.ext import commands

config = {
    'token': 'token',
    'prefix': 'prefix',
}

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.default())


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(ctx.content)


bot.run(config['token'])

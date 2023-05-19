import discord
from discord.ext import commands

config = {
    'token': 'MTA5NDcwMzYyODMxNDQ5Mjk2OA.Gjcg2q.qrCJFCHCl4VKMP3MSTSt9bh2pHS0GCyPmGU7ns',
    'prefix': 'prefix',
}

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.default())


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(ctx.content)


bot.run(config['token'])

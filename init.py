import discord
from discord.ext import commands

config = {
    'token': 'token',
    'prefix': '!',
}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command(name='test')
async def test(ctx, arg):
    print(arg)
    #if message.author != bot.user:
    #    await message.channel.send(message)


bot.run(config['token'])

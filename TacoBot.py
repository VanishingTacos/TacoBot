import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('DISCORD_TOKEN')
logChannel = os.environ.get('LOG_CHANNEL')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='.')
bot.remove_command('help')

@bot.command()
async def load(ctx, extenstion):
    bot.load_extension(f'cogs.{extenstion}')
    await ctx.send('Extenstion has been loaded')

@bot.command()
async def unload(ctx, extenstion):
    bot.unload_extension(f'cogs.{extenstion}')
    await ctx.send('Extenstion has been unloaded')

#reload all cogs or a specific cog
@bot.command()
async def reload(ctx, extenstion=None):
    if extenstion == None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send('All cogs have been reloaded')
    else:
        bot.unload_extension(f'cogs.{extenstion}')
        bot.load_extension(f'cogs.{extenstion}')
        await ctx.send('Extenstion has been reloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):

        bot.load_extension(f'cogs.{filename[:-3]}')

#get the token enviroment variable
bot.run(os.environ.get(TOKEN))
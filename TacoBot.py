import discord
from discord.ext import commands
import os
from config import *

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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(KEY)
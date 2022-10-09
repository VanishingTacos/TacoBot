import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')
logChannel = os.environ.get('LOG_CHANNEL')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='.')
bot.remove_command('help')

@bot.command()
async def load(ctx, extenstion):
    await bot.load_extension(f'cogs.{extenstion}')
    await ctx.send('Extenstion has been loaded')

@bot.command()
async def unload(ctx, extenstion):
    await bot.unload_extension(f'cogs.{extenstion}')
    await ctx.send('Extenstion has been unloaded')

#reload all cogs or a specific cog
@bot.command()
async def reload(ctx, extenstion=None):
    if extenstion == None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.unload_extension(f'cogs.{filename[:-3]}')
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send('All cogs have been reloaded')
    else:
        bot.unload_extension(f'cogs.{extenstion}')
        bot.load_extension(f'cogs.{extenstion}')
        await ctx.send('Extenstion has been reloaded')


async def load_extenstions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):

            await bot.load_extension(f'cogs.{filename[:-3]}')



async def main():
    async with bot:
        await load_extenstions()
        await bot.start(TOKEN)

asyncio.run(main())
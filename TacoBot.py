import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
logChannel = os.environ.get("LOG_CHANNEL")

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=".")
bot.remove_command("help")


@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send("Extension has been loaded")


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Extension has been unloaded")


# reload all cogs or a specific cog
@bot.command()
async def reload(ctx, extension=None):
    if extension is None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.unload_extension(f"cogs.{filename[:-3]}")
                await bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("All cogs have been reloaded")
    else:
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send("Extension has been reloaded")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())

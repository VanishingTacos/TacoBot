import discord
from discord.ext import commands
import asyncio
from config import *

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

class events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Success! We have logged in as {0.user}'.format(self.bot))
        await self.bot.change_presence(activity=discord.Game('Looking for Tacos'))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not ctx.message.content.startswith('.clear'):
            await asyncio.sleep(3)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(events(bot))
import discord
from discord.ext import commands
import asyncio
import os
import json
from datetime import datetime
from config import *

# spam detection settings
time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}


# check for warnings.json file
if not os.path.exists('./JSON/warnings.json'):
    with open('./JSON/warnings.json', 'w') as f:
        json.dump({}, f)

#load warnings.json
with open('./JSON/warnings.json', 'r') as f:
    loadWarnings = json.load(f)

# function for saving to warnings.json
def saveWarnings(warnings):
    with open('./JSON/warnings.json', 'w') as f:
        json.dump(warnings, f)

# Get current time and date
def getTime():
    return datetime.now().strftime('%m/%d/%y %I:%M:%S %p')

# make embed
def makeEmbed(color, name, value):
    embed = discord.Embed(color = color)
    embed.add_field(name = name, value = value)
    return embed

class events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Success! We have logged in as {0.user}'.format(self.bot))
        await self.bot.change_presence(activity=discord.Game('Looking for Tacos'))

    #spam prevention
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author.id in author_msg_times:
            author_msg_times[message.author.id] += 1
            if author_msg_times[message.author.id] > max_msg_per_window:
                await message.channel.send(embed = makeEmbed(discord.Color.red(), 'Spam Prevention', f'{message.author.mention} You are sending messages too fast. Slow down!'))
                author_msg_times[message.author.id] = 0
                await asyncio.sleep(time_window_milliseconds / 1000)
        else:
            author_msg_times[message.author.id] = 1


def setup(bot):
    bot.add_cog(events(bot))
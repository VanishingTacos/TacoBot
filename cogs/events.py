import discord
from discord.ext import commands
import asyncio
import os
import json
from datetime import datetime

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

#spam filter settings
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
    
    #delete command message after its executed
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.message.content.startswith('.'):
            return
        else:
            await ctx.message.delete()
    
    #on_message_delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return
        if message.channel.id == 915101965820784661:
            return
        if message.content.startswith('.'):
            return
        embed = makeEmbed(0xFF0000, "Message Deleted", f"{message.author.name}'s message was deleted in {message.channel.mention} at {getTime()} \n\n Message:\n```{message.content}```")
        await self.bot.get_channel(915101965820784661).send(embed = embed)
    
    #on_message_edit
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.author.id == self.bot.user.id:
            return
        if before.channel.id == logChannel:
            return
        embed = makeEmbed(0xFF0000, "Message Edited", f"{before.author.name}'s message was edited in {before.channel.mention} at {getTime()} \n\n Before:\n``` {before.content}``` \n\n After:\n```{after.content}```")
        await self.bot.get_channel(logChannel).send(embed = embed)

    #spam prevention
    #https://stackoverflow.com/a/64961500
    @commands.Cog.listener()
    async def on_message(self, ctx):
        global author_msg_counts

        author_id = ctx.author.id
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
            author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
            msg_time for msg_time in author_msg_times[author_id]
            if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
            author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.

        if len(author_msg_times[author_id]) > max_msg_per_window:
            await ctx.channel.send(embed = makeEmbed(0xFF0000, "Spam detected", "Please don't spam."))
            # mute the user for 1 minute
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = 'muted'))
            await asyncio.sleep(60)
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name = 'muted'))

    #on memeber leave and send message to log channel
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = makeEmbed(0xFF0000, "Member Left", f"{member.name}#{member.discriminator} has left the server at {getTime()}")
        await self.bot.get_channel(logChannel).send(embed = embed)
            
def setup(bot):
    bot.add_cog(events(bot))
import discord
from discord.ext import commands
import asyncio
import os
import json
from datetime import datetime

logChannel = os.environ.get('LOG_CHANNEL')


# Get current time and date
def get_time():
    return datetime.now().strftime('%m/%d/%y %I:%M:%S %p')


# make embed
def make_embed(color, name, value):
    embed = discord.Embed(color=color)
    embed.add_field(name=name, value=value)
    return embed


# spam filter settings
time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Success! We have logged in as {0.user}'.format(self.bot))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".help"))

    # delete command message after its executed
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.message.content.startswith('.'):
            return
        else:
            await ctx.message.delete()

    # on_message_delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return
        if message.channel.id == int(logChannel):
            return
        if message.content.startswith('.'):
            return
        embed = make_embed(0xFF0000, "Message Deleted",
                           f"{message.author.name}'s message was deleted in {message.channel.mention} at {get_time()} \n\n Message:\n```{message.content}```")
        await self.bot.get_channel(int(logChannel)).send(embed=embed)

    # on_message_edit
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        if after.author.id == self.bot.user.id:
            return
        if after.channel.id == 915101965820784661:
            return
        if after.content.startswith('.'):
            return
        embed = make_embed(0xFF0000, "Message Edited",
                           f"{after.author.name}'s message was edited in {after.channel.mention} at {get_time()} \n\n Before:\n```{before.content}```\n\n After:\n```{after.content}```")
        await self.bot.get_channel(915101965820784661).send(embed=embed)

    # spam prevention
    # https://stackoverflow.com/a/64961500
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
            await ctx.channel.send(embed=make_embed(0xFF0000, "Spam detected", "Please don't spam."))
            # mute the user for 1 minute
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name='muted'))
            await asyncio.sleep(60)
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name='muted'))

    # on memeber leave and send message to log channel
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = make_embed(0xFF0000, "Member Left",
                           f"{member.name}#{member.discriminator} has left the server at {get_time()}")
        await self.bot.get_channel(logChannel).send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))

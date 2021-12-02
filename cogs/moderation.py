#*********************************#
#   Moderation commands           #
#                                 #   
#   These should only be          #
#   available to server admins &  #
#   mods!                         #
#*********************************#

from re import DEBUG
import discord
from discord import embeds
from discord.ext import commands
import json
import os
import asyncio
from datetime import datetime
from config import *


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

# check for poll.json file
if not os.path.exists('./JSON/poll.json'):
    with open('./JSON/poll.json', 'w') as f:
        json.dump({}, f)

# load poll.json

#function to load poll.json
def _loadPolls():
    with open('./JSON/poll.json', 'r') as f:
        return json.load(f)

# function for saving to poll.json
def savePolls(poll):
    with open('./JSON/poll.json', 'w') as f:
        json.dump(poll, f)

# Get current time and date
def getTime():
    return datetime.now().strftime('%m/%d/%y %I:%M:%S %p')

# make embed
def makeEmbed(color, name, value):
    embed = discord.Embed(color = color)
    embed.add_field(name = name, value = value)
    return embed

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    
    # enable / disable slowmoade for x seconds
    @commands.command()
    @commands.has_role('new role1')
    async def slowmode(self, ctx, seconds : int = 0):
        await ctx.channel.edit(slowmode_delay = seconds)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'Slowmode set to {seconds} seconds!'))

    # give warning
    @commands.command(name = 'warn')
    @commands.has_role('new role1')
    async def warn(self, ctx, username : discord.Member, * ,note=None):
        if str(username.id) not in loadWarnings:
            loadWarnings[username.id] = []
            loadWarnings[username.id].append({
            'warned_by' : ctx.author.id,
            'time' : getTime(),
            'note' : note
        })
            # save to json
            saveWarnings(loadWarnings)
            await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been warned'))
        else:
            # add warning to user
            loadWarnings[str(username.id)].append({
            'warned_by' : ctx.author.id,
            'time' : getTime(),
            'note' : note
        })
            # save to json
            saveWarnings(loadWarnings)
            await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been warned'))

    #list warnings
    @commands.command(name = 'listwarnings')
    @commands.has_role('new role1')
    async def listwarnings(self, ctx, username : discord.Member):
        if str(username.id) not in loadWarnings:
            await ctx.send(f'{username.mention} has no warnings')
        else:
            embed = discord.Embed(title = f'{username.name} warnings', color = discord.Color.red())
            for warning in loadWarnings[str(username.id)]:
                embed.add_field(name = warning['time'], value = f'Warned by {self.bot.get_user(int(warning["warned_by"])).name}\n{warning["note"]}')
                embed.set_thumbnail(url = username.avatar_url)
            await ctx.send(embed = embed)


    # kick member
    @commands.command(name = 'kick')
    @commands.has_role('new role1')
    async def kick(self, ctx, username : discord.Member, *, reason=None):
        await username.kick(reason=reason)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Kick Success', f'{username.mention} has been kicked!'))

    # ban member
    @commands.command(name = 'ban')
    @commands.has_role('new role1')
    async def ban(self, ctx, username : discord.Member, *, reason=None):
        await username.ban(reason=reason)
        msg = await ctx.send(embed = makeEmbed(discord.Color.green(), 'Ban Succsess', f'{username.mention} has been banned!'))

    #remove only messages from a specific user
    @commands.command(name = 'purgeuser')
    @commands.has_role('new role1')
    async def purgeusers(self, ctx, username : discord.Member, int : int = 10):
        await ctx.channel.purge(limit = int, check = lambda m: m.author == username)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'✅ Messages from {username.name} has been removed!'))

    # mute member
    @commands.command(name = 'mute')
    @commands.has_role('new role1')
    async def mute(self, ctx, username : discord.Member, *, reason=None):
        
        #create muted role if it doesn't exist
        if not discord.utils.get(ctx.guild.roles, name='muted'):
            mutedRole = await ctx.guild.create_role(name='muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(mutedRole, send_messages=False)
        
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await username.add_roles(role)
        embed = discord.Embed()
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been muted!'))
    
    #temp mute member
    @commands.command(name = 'tempmute')
    @commands.has_role('new role1')
    async def tempmute(self, ctx, username : discord.Member, time : int, units, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await username.add_roles(role)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been muted for {time} seconds!'))
        await asyncio.sleep(time)
        await username.remove_roles(role)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been unmuted!'))
    
    # unmute member
    @commands.command(name = 'unmute')
    @commands.has_role('new role1')
    async def unmute(self, ctx, username : discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await username.remove_roles(role)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} has been unmuted!'))
    
    # unban member
    @commands.command(name = 'unban')
    @commands.has_role('new role1')
    async def unban(self, ctx, *, username):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user)
            await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'✅ {user.mention} has been unbanned!'))
    
    # change nickname
    @commands.command(name = 'nickname')
    @commands.has_role('new role1')
    async def nickname(self, ctx, username : discord.Member, *, nickname):
        await username.edit(nick = nickname)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} nickname has been changed to {nickname}'))
    
    # remove nickname
    @commands.command(name = 'removenickname')
    @commands.has_role('new role1')
    async def removenickname(self, ctx, username : discord.Member):
        await username.edit(nick = None)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'{username.mention} nickname has been removed'))

    # remove all warnings from member
    @commands.command(name = 'clearallwarnings')
    @commands.has_role('new role1')
    async def clearallwarnings(self, ctx, username : discord.Member):
        if str(username.id) not in loadWarnings:
            await ctx.send(f'{username.mention} has no warnings')
        else:
            del loadWarnings[str(username.id)]
            saveWarnings(loadWarnings)
            await ctx.send(f'{username.mention} warnings have been cleared')

    # purge messages
    @commands.command(name = 'purge')
    @commands.has_role('new role1')
    async def purge(self, ctx: commands.Context, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'✅ {amount} messages have been purged!'))
        await asyncio.sleep(3)
        await msg.delete()    
    
    # show infomation about a member
    @commands.command(name = 'userinfo')
    @commands.has_role('new role1')
    async def userinfo(self, ctx, username : discord.Member):
        embed = discord.Embed(color = discord.Color.red())
        embed.add_field(name = 'Username', value = username.name)
        embed.add_field(name = 'ID', value = username.id)
        embed.add_field(name = 'Nickname', value = username.nick)
        embed.add_field(name = 'Status', value = username.status)
        embed.add_field(name = 'Joined At', value = username.joined_at)
        embed.add_field(name = 'Created At', value = username.created_at)
        embed.add_field(name = 'Top Role', value = username.top_role)
        embed.set_thumbnail(url = username.avatar_url)
        embed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    # create poll
    @commands.command(name = 'poll')
    @commands.has_role('new role1')
    async def poll(self, ctx, *, question):
        
        # check if a poll in poll.json has the status of 'open'
        # if it does, then the bot will not create another poll
        # if it doesn't, then the bot will create a new poll

        def makePoll(question):
            embed = discord.Embed(title = 'Poll', color = discord.Color.green())
            embed.add_field(name = 'Question', value = question)
            return embed
        
        loadPolls = _loadPolls()
        msg = await ctx.send(embed = makePoll(question))
        
        try: 
            latestPollID = loadPolls['latestPollID']
        except:
            latestPollID = 0
        
        if len(loadPolls) == 0:
            loadPolls['latestPollID'] = msg.id
            loadPolls[msg.id] = [{
                'question': question,
                'status': 'open',
                'reactions': [],
                'author': ctx.author.id,
                'channel': ctx.channel.id
            }]
            savePolls(loadPolls)

            await msg.add_reaction('✅')
            await msg.add_reaction('❌')

        elif loadPolls[str(latestPollID)][0]['status'] == 'open':
                await msg.delete()
                await ctx.send(embed = makeEmbed(discord.Color.red(), 'Error', 'A poll is already open!'))
        else:
            loadPolls['latestPollID'] = msg.id
            loadPolls[msg.id] = [{
                'question': question,
                'status': 'open',
                'reactions': [],
                'author': ctx.author.id,
                'channel': ctx.channel.id
            }]
            savePolls(loadPolls)
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
    
    # close poll and get total number of checks and crosses
    @commands.command(name = 'closepoll')
    @commands.has_role('new role1')
    async def closepoll(self, ctx):
        loadPolls = _loadPolls()

        try:
            latestPollID = loadPolls['latestPollID']
        except:
            latestPollID = 0
        
        if len(loadPolls) == 0:
            await ctx.send(embed = makeEmbed(discord.Color.red(), 'Error', 'There is no poll to close!'))
        elif loadPolls[str(latestPollID)][0]['status'] == 'closed':
            await ctx.send(embed = makeEmbed(discord.Color.red(), 'Error', 'There is no poll to close!'))
        else:
            loadPolls[str(latestPollID)][0]['status'] = 'closed'
            savePolls(loadPolls)

            # get total number of checks and crosses
            getPoll = await ctx.fetch_message(latestPollID)
            
            for reaction in getPoll.reactions:
                if reaction.emoji == '✅':
                    checks = reaction.count - 1
                elif reaction.emoji == '❌':
                    crosses = reaction.count - 1

            emebed = discord.Embed(title = 'Poll Results', color = discord.Color.green())
            emebed.add_field(name = 'Question', value = loadPolls[str(latestPollID)][0]['question'], inline = False)
            emebed.add_field(name = '✅', value = checks)
            emebed.add_field(name = '❌', value = crosses)
            emebed.add_field(name = 'Total', value = checks + crosses)
            await ctx.send(embed = emebed)

    # say something
    @commands.command(name = 'say')
    @commands.has_role('new role1')
    async def say(self, ctx, *, message):
        await ctx.send(message)
    

    # add role
    @commands.command(name = 'addrole')
    @commands.has_role('new role1')
    async def addrole(self, ctx, username : discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        await username.add_roles(role)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Success', f'✅ {role} has been added to {username.mention}'))
    
    # remove role
    @commands.command(name = 'removerole')
    @commands.has_role('new role1')
    async def removerole(self, ctx, username : discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        print(role)
        await username.remove_roles(role)
        await ctx.send(embed = makeEmbed(discord.Color.red(), 'Role Removed', f'{role} has been removed from {username.mention}'))
    
    # create new role
    @commands.command(name = 'createrole')
    @commands.has_role('new role1')
    async def createrole(self, ctx, *, role):
        await ctx.guild.create_role(name = role)
        await ctx.send(embed = makeEmbed(discord.Color.green(), 'Role Created', f'{role} has been created'))
    
    # delete role from server
    @commands.command(name = 'deleterole')
    @commands.has_role('new role1')
    async def deleterole(self, ctx, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        await role.delete()
        await ctx.send(embed = makeEmbed(discord.Color.red(), 'Role Deleted', f'{role} has been deleted'))
    
    # create new text or voice channel
    @commands.command(name = 'createchannel')
    @commands.has_role('new role1')
    async def createchannel(self, ctx, type, *, channel):
        if type == 'text':
            await ctx.guild.create_text_channel(channel)
            await ctx.send(embed = makeEmbed(discord.Color.green(), 'Channel Created', f'{channel} has been created'))
        elif type == 'voice':
            await ctx.guild.create_voice_channel(channel)
            await ctx.send(embed = makeEmbed(discord.Color.green(), 'Channel Created', f'{channel} has been created'))
        else:
            await ctx.send(embed = makeEmbed(discord.Color.red(), 'Error', 'Please enter a valid type'))

    # delete channel
    @commands.command(name = 'deletechannel')
    @commands.has_role('new role1')
    async def deletechannel(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.channels, name = channel)
        print(channel)
        await channel.delete()
        await ctx.send(embed =  makeEmbed(discord.Color.red(), 'Channel Deleted', f'{channel} has been deleted'))
    
    #list channels
    @commands.command(name = 'listchannels')
    @commands.has_role('new role1')
    async def listchannels(self, ctx):
        for channel in ctx.guild.channels:
            await ctx.send(f'{channel}')




def setup(bot):
    bot.add_cog(moderation(bot))

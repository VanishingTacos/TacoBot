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
            await ctx.send(f'{username.mention} has been warned')
        else:
            # add warning to user
            loadWarnings[str(username.id)].append({
            'warned_by' : ctx.author.id,
            'time' : getTime(),
            'note' : note
        })
            # save to json
            saveWarnings(loadWarnings)
            await ctx.send(f'{username.mention} has been warned')

    @commands.command(name = 'listwarnings')
    @commands.has_role('new role1')
    async def listwarnings(self, ctx, username : discord.Member):
        if str(username.id) not in loadWarnings:
            await ctx.send(f'{username.mention} has no warnings')
        else:
            embed = discord.Embed(title = f'{username.name} warnings', color = discord.Color.red())
            print(username.avatar_url)
            for warning in loadWarnings[str(username.id)]:
                embed.add_field(name = warning['time'], value = f'Warned by {self.bot.get_user(int(warning["warned_by"])).name}\n{warning["note"]}')
                embed.set_thumbnail(url = username.avatar_url)
            await ctx.send(embed = embed)


    # kick member
    @commands.command(name = 'kick')
    @commands.has_role('new role1')
    async def kick(self, ctx, username : discord.Member, *, reason=None):
        await username.kick(reason=reason)
        embed = discord.Embed()
        embed.add_field(name = 'Kick Succsess', value = f'{username.mention} has been kicked!')
        await ctx.send(embed = embed)

    # ban member
    @commands.command(name = 'ban')
    @commands.has_role('new role1')
    async def ban(self, ctx, username : discord.Member, *, reason=None):
        await username.ban(reason=reason)
        embed = discord.Embed()
        embed.add_field(name = 'Ban Succsess', value = f'✅ {username.mention} has been banned!')
        msg = await ctx.send(embed = embed)

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
        embed.add_field(name = 'Mute Succsess', value = f'{username.mention} has been muted!')
        await ctx.send(embed = embed)
    
    # unmute member
    @commands.command(name = 'unmute')
    @commands.has_role('new role1')
    async def unmute(self, ctx, username : discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name='muted')
        await username.remove_roles(role)
        embed = discord.Embed()
        embed.add_field(name = 'Unmute Succsess', value = f'{username.mention} has been unmuted!')
        await ctx.send(embed = embed)
    
    # unban member
    @commands.command(name = 'unban')
    @commands.has_role('new role1')
    async def unban(self, ctx, *, username):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user)
            embed = discord.Embed()
            embed.add_field(name = 'Unban Succsess', value = f'✅ {user.mention} has been unbanned!')
            msg = await ctx.send(embed = embed)

    # remove all warnings from member
    @commands.command(name = 'clearallwarnings')
    @commands.has_role('new role1')
    async def clearallwarnings(self, ctx, username : discord.Member):
        if str(username.id) not in loadWarnings:
            await ctx.send(f'{username.mention} has no warnings')
        else:
            loadWarnings[str(username.id)] = []
            saveWarnings(loadWarnings)
            await ctx.send(f'{username.mention} warnings have been cleared')

    # purge messages
    @commands.command(name = 'clear')
    @commands.has_role('new role1')
    async def clear(self, ctx: commands.Context, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(color = 0x32CD32)
        embed.add_field(name = 'Succsess', value = f'✅ {amount} messages have been purged!')
        msg = await ctx.send(embed = embed)
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
        embed = discord.Embed(title = 'Poll', description = question, color = discord.Color.purple())
        msg = await ctx.send(embed = embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

    # add role
    @commands.command(name = 'addrole')
    @commands.has_role('new role1')
    async def addrole(self, ctx, username : discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        await username.add_roles(role)
        embed = discord.Embed(title = 'Role Added', description = f'{role} has been added to {username.mention}', color = discord.Color.green())
        await ctx.send(embed = embed)
    
    # remove role
    @commands.command(name = 'removerole')
    @commands.has_role('new role1')
    async def removerole(self, ctx, username : discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        print(role)
        await username.remove_roles(role)
        embed = discord.Embed(title = 'Role Removed', description = f'{role} has been removed from {username.mention}', color = discord.Color.red())
        await ctx.send(embed = embed)
    
    # create new role
    @commands.command(name = 'createrole')
    @commands.has_role('new role1')
    async def createrole(self, ctx, *, role):
        await ctx.guild.create_role(name = role)
        embed = discord.Embed(title = 'Role Created', description = f'{role} has been created', color = discord.Color.green())
        await ctx.send(embed = embed)
    
    # delete role from server
    @commands.command(name = 'deleterole')
    @commands.has_role('new role1')
    async def deleterole(self, ctx, *, role):
        role = discord.utils.get(ctx.guild.roles, name = role)
        await role.delete()
        embed = discord.Embed(title = 'Role Deleted', description = f'{role} has been deleted', color = discord.Color.red())
        await ctx.send(embed = embed)
    
    # create new text channel
    @commands.command(name = 'createchannel')
    @commands.has_role('new role1')
    async def createchannel(self, ctx, *, channel):
        await ctx.guild.create_text_channel(channel)
        embed = discord.Embed(title = 'Channel Created', description = f'{channel} has been created', color = discord.Color.green())
        await ctx.send(embed = embed)
    
    #create new voice channel
    @commands.command(name = 'createvoicechannel')
    @commands.has_role('new role1')
    async def createvoicechannel(self, ctx, *, channel):
        await ctx.guild.create_voice_channel(channel)
        embed = discord.Embed(title = 'Channel Created', description = f'{channel} has been created', color = discord.Color.green())
        await ctx.send(embed = embed)

    # delete channel
    @commands.command(name = 'deletechannel')
    @commands.has_role('new role1')
    async def deletechannel(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.channels, name = channel)
        await channel.delete()
        embed = discord.Embed(title = 'Channel Deleted', description = f'{channel} has been deleted', color = discord.Color.red())
        await ctx.send(embed = embed)




def setup(bot):
    bot.add_cog(moderation(bot))
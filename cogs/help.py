import discord
from discord.ext import commands
from config import *

class _help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    # custom help command
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title = 'TacoBot Commands', color = ctx.author.color)
        embed.add_field(name = 'Commands', value = '`.help commands`')
        embed.add_field(name = 'Fun', value = '`.help fun`')
        embed.add_field(name = 'Moderation', value = '`.help moderation`')
        await ctx.send(embed = embed)
        
    @help.command()
    async def moderation(self, ctx):
        embed = discord.Embed(title = 'Moderation Commands', color = discord.Color.green())
        embed.add_field(name = '`.ban @user`', value = 'Bans the user', inline = False)
        embed.add_field(name = '`.unban @user`', value = 'Unbans the user', inline = False)
        embed.add_field(name = '`.kick @user`', value = 'Kicks the user', inline = False)
        embed.add_field(name = '`.purge [number]`', value = 'Deletes the number of messages specified', inline = False)
        embed.add_field(name = '`.purgeuser @user [number]`', value = 'Deletes the number of messages specified from the user', inline = False)
        embed.add_field(name = '`.mute @user`', value = 'Mutes the user', inline = False)
        embed.add_field(name = '`.tempmute @user [seconds]`', value = 'Temporarily mutes the user', inline = False)
        embed.add_field(name = '`.unmute @user`', value = 'Unmutes the user', inline = False)
        embed.add_field(name = '`.warn @user`', value = 'Warns the user', inline = False)
        embed.add_field(name = '`.slowmode [seconds]`', value = 'Sets the slowmode to the number of seconds specified', inline = False)
        embed.add_field(name = '`.nickname @user [nickname]`', value = 'Changes the nickname of the user', inline = False)
        embed.add_field(name = '`.removenickname @user`', value = 'Removes the nickname of the user', inline = False)
        embed.add_field(name = '`.clearallwarnings @user`', value = 'Clears all the warnings of the user', inline = False)
        embed.add_field(name = '`.listwarnings @user`', value = 'Lists all the warnings of the user', inline = False)
        embed.add_field(name = '`.userinfo @user`', value = 'Gives information about the user', inline = False)
        embed.add_field(name = '`.serverinfo`', value = 'Gives information about the server', inline = False)
        embed.add_field(name = '`.poll [question]`', value = 'Creates a poll', inline = False)
        embed.add_field(name = '`.say [message]`', value = 'Sends the message specified', inline = False)
        embed.add_field(name = '`.addrole @user [role]`', value = 'Adds the role to the user', inline = False)
        embed.add_field(name = '`.removerole @user [role]`', value = 'Removes the role from the user', inline = False)





        await ctx.send(embed = embed)



    #========# moderation commands #========#
    
    @help.command()
    async def warn(self, ctx):
        help = '`.warn [user] [reason]`'
        embed = discord.Embed(title = 'Warn', description = 'Gives a warning a warning to a user')
        embed.add_field(name = '**Syntax**', value = '`.warn [member to warn]`')
        await ctx.send(embed = embed)


    @help.command()
    async def kick(self, ctx):
        embed = discord.Embed(title = 'Kick', description = 'Kicks user from server')
        embed.add_field(name = '**Syntax**', value = '`.kick [member to kick] optional:[reason]`')
        await ctx.send(embed = embed)

    @help.command()
    async def ban(self, ctx):
        embed = discord.Embed(title = 'Ban', description = 'Bans user from server')
        embed.add_field(name = '**Syntax**', value = '`.warn [member to ban] optional:[reason]`')
        await ctx.send(embed = embed)

    @help.command()
    async def clearallwarnings(self, ctx):
        embed = discord.Embed(title = 'Clear All Warnings', description= 'Clears all records of warnings from user')
        embed.add_field(name = '**Syntax**', value = '`.clearallwarnings [member to clear of warnings]`')
        await ctx.send(embed = embed)

    @help.command()
    async def slowmode(self, ctx):
        embed = discord.Embed(title = 'Slowmode', description= 'Sets slowmode for a channel')
        embed.add_field(name = '**Syntax**', value = '`.slowmode [channel] [number of seconds]`')
        await ctx.send(embed = embed)
    
    @help.command()
    async def listwarnings(self, ctx):
        embed = discord.Embed(title = 'List Warnings', description= 'Lists all warnings for a user')
        embed.add_field(name = '**Syntax**', value = '`.listwarnings [member to list]`')
        await ctx.send(embed = embed)
        await ctx.send(embed = embed)

    @help.command()
    async def mute(self, ctx):
        embed = discord.Embed(title = 'Mute', description= 'Mutes a user')
        embed.add_field(name = '**Syntax**', value = '`.mute [member to mute]`')
        await ctx.send(embed = embed)

    @help.command()
    async def unmute(self, ctx):
        embed = discord.Embed(title = 'Unmute', description= 'Unmutes a user')
        embed.add_field(name = '**Syntax**', value = '`.unmute [member to unmute]`')
        await ctx.send(embed = embed)

    @help.command()
    async def tempmute(self, ctx):  
        embed = discord.Embed(title = 'Tempmute', description= 'Temporarily mutes a user')
        embed.add_field(name = '**Syntax**', value = '`.tempmute [member to mute] [number of seconds]`')
        await ctx.send(embed = embed)

    @help.command()
    async def unban(self, ctx):
        embed = discord.Embed(title = 'Unban', description= 'Unbans a user')
        embed.add_field(name = '**Syntax**', value = '`.unban [member to unban]`')
        await ctx.send(embed = embed)

    @help.command()
    async def nickname(self, ctx):
        embed = discord.Embed(title = 'Nickname', description= 'Changes nickname of a user')
        embed.add_field(name = '**Syntax**', value = '`.nickname [member to change] [new nickname]`')
        await ctx.send(embed = embed)

    @help.command()
    async def removenickname(self, ctx):    
        embed = discord.Embed(title = 'Remove Nickname', description= 'Removes nickname of a user')
        embed.add_field(name = '**Syntax**', value = '`.removenickname [member to remove nickname]`')
        await ctx.send(embed = embed)

    @help.command()
    async def purge(self, ctx): 
        embed = discord.Embed(title = 'Clear', description= 'Purges messages')
        embed.add_field(name = '**Syntax**', value = '`.purge [number of messages to purge]`')
        await ctx.send(embed = embed)
    
    @help.command()
    async def purgeuser(self, ctx):
        embed = discord.Embed(title = 'Purge User', description= 'Purges all messages from a user')
        embed.add_field(name = '**Syntax**', value = '`.purgeuser [member to purge] [number of messages to purge]`')
        await ctx.send(embed = embed)

    @help.command()
    async def userinfo(self, ctx):
        embed = discord.Embed(title = 'User Info', description= 'Shows infomation about a user')
        embed.add_field(name = '**Syntax**', value = '`.userinfo [member to show]`')
        await ctx.send(embed = embed)

    @help.command()
    async def poll(self, ctx):
        embed = discord.Embed(title = 'Poll', description= 'Creates a poll')
        embed.add_field(name = '**Syntax**', value = '`.poll [question] [option 1] [option 2] ... [option n]`')
        await ctx.send(embed = embed)

    @help.command()
    async def say(self, ctx):
        embed = discord.Embed(title = 'Say', description= 'Makes the bot say something')
        embed.add_field(name = '**Syntax**', value = '`.say [message]`')
    
    @help.command()
    async def addrole(self, ctx):
        embed = discord.Embed(title = 'Add Role', description= 'Adds a role to a user')
        embed.add_field(name = '**Syntax**', value = '`.addrole [member to add role to] [role to add]`')
    
    @help.command()
    async def deleterole(self, ctx):
        embed = discord.Embed(title = 'Delete Role', description= 'Deletes a role from a user')
        embed.add_field(name = '**Syntax**', value = '`.removerole [member to delete role from] [role to delete]`')
        await ctx.send(embed = embed)

    @help.command()
    async def deletechannel(self, ctx):
        embed = discord.Embed(title = 'Delete Channel', description= 'Deletes a channel')
        embed.add_field(name = '**Syntax**', value = '`.deletechannel [channel to delete]`')
        await ctx.send(embed = embed)

    @help.command()
    async def createchannel(self, ctx):
        embed = discord.Embed(title = 'Create Channel', description= 'Creates a channel')
        embed.add_field(name = '**Syntax**', value = '`.createchannel [voice or text] [channel name]`')
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(_help(bot))
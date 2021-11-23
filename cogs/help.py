import discord
from discord.ext import commands
from config import *

class _help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    # custom help command
    @commands.group(invoke_without_command = True)
    async def help(self, ctx):
        embed = discord.Embed(title = 'Help', description = 'Use .help [command name] for more infomation', color = ctx.author.color)
        embed.add_field(name = 'Moderation', value = 'warn, kick, ban, clearallwarnings, clear, userinfo')

        await ctx.send(embed = embed)

    @help.command()
    async def warn(self, ctx):
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
    async def clear(self, ctx):
        embed = discord.Embed(title = 'Clear', description= 'Purges messages')
        embed.add_field(name = '**Syntax**', value = '`.clear [number of messages to purge]`')

        await ctx.send(embed = embed)

    @help.command()
    async def userinfo(self, ctx):
        embed = discord.Embed(title = 'User Info', description= 'Shows infomation about a user')
        embed.add_field(name = '**Syntax**', value = '`.userinfo [member to show]`')

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(_help(bot))
import discord
from discord.ext import commands
import asyncio
from config import *


class _commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #### commands ####

    # bot latency check
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Took {round(self.bot.latency, 3)}')

    # shows infomation the server
    @commands.command(name = 'serverinfo')
    async def serverinfo(self, ctx):
        guild = self.bot.get_guild(ctx.guild.id)
        online = 0
        memberlist = guild.members
        for member in memberlist:
            if str(member.status) == 'online':
                online += 1   
        bot_list = len([bot.mention for bot in ctx.guild.members if bot.bot])
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        roles = len(ctx.guild.roles)
        channels = text_channels + voice_channels
        embed = discord.Embed(color = ctx.guild.owner.top_role.color)
        (
            embed
            .add_field(name = 'Owner', value = ctx.guild.owner)
            .add_field(name = 'Members', value = f'{ctx.guild.member_count} members,\n {online} online\n {bot_list} bots, {ctx.guild.member_count - bot_list} humans')
            .add_field(name = 'Total Channels', value = f'{channels} total channels:\n {categories} categories\n {text_channels} text, {voice_channels} voice',)
            .add_field(name = 'Total Roles', value = f'{roles}',)
            .add_field(name = 'Server Created', value = ctx.guild.created_at.strftime('%a, %d %b %Y \n %H:%M:%S %ZGMT'),)
            .set_thumbnail(url = str(ctx.guild.icon_url))
            .set_footer(text = f'{guild} | {ctx.guild.id}')
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(_commands(bot))


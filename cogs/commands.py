import discord
from discord.ext import commands
import asyncio

class _commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #### commands ####

    # bot latency check
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    # shows infomation the server
    @commands.command(name = 'serverinfo')
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f'{ctx.guild.name}', description=f'Server ID: {ctx.guild.id}', color=0x00ff00)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Owner', value=ctx.guild.owner)
        embed.add_field(name='Members', value=ctx.guild.member_count)
        embed.add_field(name='Created', value=ctx.guild.created_at.strftime('%a, %d %b %Y \n %H:%M:%S %ZGMT'))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.add_field(name='Channels', value=len(ctx.guild.channels))
        embed.add_field(name='Emojis', value=len(ctx.guild.emojis))
        embed.add_field(name='Verification Level', value=ctx.guild.verification_level)
        print(ctx.guild.verification_level)
        embed.add_field(name='Explicit Content Filter', value=ctx.guild.explicit_content_filter)
        await ctx.send(embed=embed)

    # shows infomation about the bot
    @commands.command(name = 'botinfo')
    async def botinfo(self, ctx):
        embed = discord.Embed(color = 0x00ff00)
        embed.add_field(name = 'Bot Name', value = self.bot.user.name)
        embed.add_field(name = 'Bot ID', value = self.bot.user.id)
        embed.add_field(name = 'Bot Version', value = '1.0.0')
        embed.add_field(name = 'Bot Owner', value = 'VanishingTacos#1391')
        embed.add_field(name = 'Bot Created', value = self.bot.user.created_at.strftime('%a, %d %b %Y \n %H:%M:%S %ZGMT'))
        embed.add_field(name = 'Bot Latency', value = f'{round(self.bot.latency, 3)}')
        embed.set_thumbnail(url = str(self.bot.user.avatar_url))
        await ctx.send(embed = embed)
    
    #create bot invite link
    @commands.command(name = 'invite')
    async def invite(self, ctx):
        await ctx.send(f'Invite me to your server: {discord.utils.oauth_url(self.bot.user.id)}')
def setup(bot):
    bot.add_cog(_commands(bot))


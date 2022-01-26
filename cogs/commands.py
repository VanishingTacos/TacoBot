import discord
from discord.ext import commands
import datetime
import pytz

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
        embed.add_field(name='Owner', value=ctx.guild.owner.name)
        embed.add_field(name='Members', value=ctx.guild.member_count)
        # get number of online members
        online = 0
        for member in ctx.guild.members:
            if member.status == discord.Status.online or member.status == discord.Status.idle:
                online += 1
        embed.add_field(name='Online', value=online)
        embed.add_field(name='Created', value=ctx.guild.created_at.strftime('%a, %d %b %Y \n %H:%M:%S %ZGMT'))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        # get the number of channels
        text_channels = 0
        voice_channels = 0
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                text_channels += 1
            elif isinstance(channel, discord.VoiceChannel):
                voice_channels += 1
        embed.add_field(name='Channels', value=f'{text_channels} text, {voice_channels} voice')
        embed.add_field(name='Emojis', value=len(ctx.guild.emojis))
        embed.add_field(name='Verification Level', value=ctx.guild.verification_level)
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

    # convert a user specified timezone to a different timezone that the user specified using timedelta
    @commands.command(name = 'timedelta')
    async def timedelta(self, ctx, timezone1: str, timezone2: str, *, time: str):
        timezone1 = pytz.timezone(timezone1)
        timezone2 = pytz.timezone(timezone2)
        time1 = datetime.datetime.strptime(time, '%Y-%m-%d %I:%M %p')
        time2 = timezone1.localize(time1)
        time3 = time2.astimezone(timezone2)
        embed = discord.Embed(title = 'Time Delta', color = 0x00ff00)
        embed.add_field(name = 'Time', value = f'{time2.strftime("%Y-%m-%d %I:%M %p %Z")} is {time3.strftime("%Y-%m-%d %I:%M %p")} in {timezone2}')
        await ctx.send(embed=embed)
            
    # using timezone abbrv convert users time to that timezone
    @commands.command(name = 'time')
    async def time(self, ctx, *, timezone):
        # list all timezones
        # timezones = pytz.all_timezones
        # print(timezones)
        #get the timezone abbrv
        tz = pytz.timezone(timezone)
        # get the current time in that timezone
        time = datetime.datetime.now(tz=tz)
        # send the time
        await ctx.send(f'The time in {timezone} is {time.strftime("%H:%M/%I:%M %p")}')

    # list common timezones
    @commands.command(name = 'timezones')
    async def timezones(self, ctx):
        timezone = pytz.common_timezones
        print(timezone)




def setup(bot):
    bot.add_cog(_commands(bot))


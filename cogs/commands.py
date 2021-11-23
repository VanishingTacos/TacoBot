import discord
from discord.ext import commands
import mysql.connector
import asyncio
from config import *

# connect to database
db = mysql.connector.connect(
    host=hostname,
    user=user,
    passwd=password,
    database=database
)

curr = db.cursor()

# are we connected?
try:
    db.connect()
    print('Connected to database')
except:
    exit('DB connection error')


class _commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #### commands ####

    # bot latency check
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Took {round(self.bot.latency, 3)}')

    # enable / disable slowmoade for x seconds
    @commands.command()
    @commands.has_role('new role1')
    async def slowmode(self, ctx, seconds : int = 0):
        await ctx.channel.edit(slowmode_delay = seconds)
        if seconds != 0:
            await ctx.send(f'Slowmode has set to {seconds} seconds')
        else: 
            await ctx.send('Slowmode has been disabled ')

    # give warning
    @commands.command(name = 'warn')
    @commands.has_role('new role1')
    async def warn(self, ctx, username : discord.Member):

        curr.execute("SELECT * from users WHERE username=%s", (str(username),))
        results = curr.fetchall()
        if len(results) == 0:
            if username.id:
                embed = discord.Embed(color = 0xFF0000)
                embed.add_field(name = 'Warning Notice', value = f'‼️ {username.mention} you have been warned!')
                await ctx.send(embed=embed)
                l = curr.execute('INSERT INTO users (user_id, username, been_warned, warned_date, warned_times) VALUES (%s,%s,%s,%s,%s)',(
                    int(username.id),
                    str(username),
                    'yes',
                    get_datetime(),
                    1
                ))

                db.commit()
        else:
            if username.id:
                curr.execute('SELECT warned_times FROM users WHERE username = %s LIMIT 1', (str(username),))
                result = curr.fetchall()[0][0]
                if result:
                    result = result
                else:
                    result = 0
                embed = discord.Embed(color = 0xFF0000)
                embed.add_field(name = 'Warning Notice', value = f'‼️ {username.mention} you have been warned {result + 1} times!')
                await ctx.send(embed=embed)
                curr.execute('UPDATE users SET warned_times=%s WHERE username=%s', (result +1,str(username)))
                db.commit()
    
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
        embed.add_field(name = 'Ban Succsess', value = f'{username.mention} has been banned!')
        await ctx.send(embed = embed)

    # remove all warnings from member
    @commands.command(name = 'clearallwarnings')
    @commands.has_role('new role1')
    async def clearallwarnings(self, ctx, username : discord.Member):
        curr.execute('SELECT warned_times FROM users WHERE username=%s', (str(username),))
        result = curr.fetchall()

        if result[0] != (None,):
            curr.execute('UPDATE users SET warned_times=%s WHERE username=%s', (None,str(username)))
            db.commit()
            embed = discord.Embed(color = 0x32CD32)
            embed.add_field(name = 'Succsess', value = f'✅ All warnings for {username.name} have been removed!')
            await ctx.send(embed=embed)
        else:
            print('debug')

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
        curr.execute('SELECT * FROM users WHERE username = %s', (str(username),))
        results = curr.fetchall()


        if results != []:
            warned_times = results[0][5]
        else:
            warned_times = None

        perm_list = len([perm[0] for perm in username.guild_permissions if perm[1]])
        role_list = [r.name for r in username.roles if r != ctx.guild.default_role]
        roles = ', '.join(role_list)

        if len(roles) == 0:
            roles = None
        else:
            roles = roles


        embed = discord.Embed(title = username.name + ' Info')
        (   
            embed
            .add_field(name = 'ID', value = username.id, inline = True)
            .add_field(name = 'Roles', value = roles)
            .add_field(name = 'Permissions', value = perm_list, inline = True)
            .add_field(name = 'Warnings', value = warned_times, inline = True)
            .add_field(name = 'Joined Server', value = username.joined_at.strftime('%m/%d/%Y \n %I:%M %p'))
            .add_field(name = 'Created account', value = username.created_at.strftime('%m/%d/%Y \n %I:%M %p'))
            .set_thumbnail(url = username.avatar_url)
            .set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
        )
        await ctx.send(embed=embed)

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
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required arguments')

def setup(bot):
    bot.add_cog(_commands(bot))


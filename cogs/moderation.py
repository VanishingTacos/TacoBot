#*********************************#
#   Moderation commands           #
#                                 #   
#   These should only be          #
#   available to server admins &  #
#   mods!                         #
#*********************************#

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

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    
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
        embed.add_field(name = 'Ban Succsess', value = f'✅ {username.mention} has been banned!')
        msg = await ctx.send(embed = embed)
    
    # unban member
    @commands.command(name = 'unban')
    @commands.has_role('new role1')
    async def unban(self, ctx, *, username):
        print('debug')
        banned_users = await ctx.guild.bans()
        username_name, username_discriminator = username.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (username_name, username_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}!')


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
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await msg.delete()
        else:
            embed = discord.Embed(color = 0xFF0000)
            embed.add_field(name = 'No warnings', value = f'❌ {username.name} has no warnings to remove!')
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await msg.delete()

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




def setup(bot):
    bot.add_cog(moderation(bot))
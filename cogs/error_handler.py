import discord
from discord.ext import commands
import mysql.connector
import re
from config import *

class _error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required arguments')
        
        elif isinstance(error, commands.BadArgument):

            if ctx.message.content.startswith('.clear') and not re.match(r'.clearallwarnings', ctx.message.content):
                await ctx.invoke(self.bot.get_command('help clear'))
            
            elif ctx.message.content.startswith('.userinfo'):
               embed = discord.Embed(color = 0xFF0000)
               embed.add_field(name = '❌ Member not found!', value = 'Please enter a vaild member name.')
               await ctx.send(embed=embed)
            
            elif ctx.message.content.startswith('.clearallwarnings'):
                await ctx.invoke(self.bot.get_command('help clearallwarnings'))

        
        elif isinstance(error, commands.CommandNotFound):
            print('Command not found')
        



def setup(bot):
    bot.add_cog(_error(bot))

import discord
from discord.ext import commands
import mysql.connector
from config import *

class _error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print('debug')
    
    
    
    
    #async def cog_command_error(self, ctx, error):
        #if isinstance(error, commands.MissingRequiredArgument):
            #print('debug')
            #await ctx.send("Missing argument(s)!")
            #return



def setup(bot):
    bot.add_cog(_error(bot))

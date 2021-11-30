import discord
from discord.ext import commands

def makeEmbed(Color, Title, Description, footer):
    embed = discord.Embed(title=Title, description=Description, color=Color)
    embed.set_footer(text=footer)
    return embed

class _error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = makeEmbed(0xFF0000, "Command not found", "The command you tried to use was not found.", None)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = makeEmbed(0xFF0000, "Missing required argument", "You are missing a required argument.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = makeEmbed(0xFF0000, "Missing permissions", "You are missing permissions to use this command.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = makeEmbed(0xFF0000, "Missing permissions", "I am missing permissions to use this command.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = makeEmbed(0xFF0000, "Command on cooldown", "This command is on cooldown. Try again in {} seconds.".format(round(error.retry_after, 2)), None)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.UserInputError):
            embed = makeEmbed(0xFF0000, "Invalid argument", "An invalid argument was passed to the command.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ArgumentParsingError):
            embed = makeEmbed(0xFF0000, "Argument parsing error", "An error occured while parsing the arguments.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = makeEmbed(0xFF0000, "Check failure", "The check you used failed.", error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            embed = makeEmbed(0xFF0000, "Command invoke error", "An error occured while invoking the command.", error)
            await ctx.send(embed=embed)
        
        
        



def setup(bot):
    bot.add_cog(_error(bot))

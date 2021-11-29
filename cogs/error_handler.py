import discord
from discord.ext import commands

def makeEmbed(Color, Title, Description):
    return discord.Embed(title=Title, description=Description, color=Color)

class _error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Missing argument", f"{error}"))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Missing permissions", f"{error}"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Bad argument", f"{error}"))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "On cooldown", f"{error}"))
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Command invoke error", f"{error}"))
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Check failure", f"{error}"))
        elif isinstance(error, commands.CommandError):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Command error", f"{error}"))
        elif isinstance(error, commands.UserInputError):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "User input error", f"{error}"))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(embed = makeEmbed(discord.Color.red(), "Command not found", f"{error}"))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(embed = makeEmbed("No private message", f"{error}"))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed = makeEmbed("Bot missing permissions", f"{error}"))
        
        



def setup(bot):
    bot.add_cog(_error(bot))

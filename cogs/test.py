import discord
from discord import app_commands
from discord.ext import commands


class SlashTest(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=discord.Object(id=911372583235092480))
        await ctx.send(f'Synced {len(fmt)} commands!')

    @app_commands.command(name='test', description='This is a test slash command')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hello World', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SlashTest(bot))

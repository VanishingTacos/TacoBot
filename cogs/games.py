import discord
from discord.ext import commands
import random

def makeembed(title, description, color, thumbnail):
    embed = discord.Embed(title=title, description=description, color=color)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed

class tictactoe(commands.Cog):

    def __init__(self, commands):
        self.commands = commands

    #flip a coin
    @commands.command(name='flip', aliases=['coin'])
    async def flip(self, ctx):
        coin = random.choice(['heads', 'tails'])
        if coin == 'heads':
            await ctx.send(embed=makeembed('Coin Flip', 'Heads', discord.Color.green(), 'https://www.nicepng.com/png/full/395-3951330_thecoinspot-com-us-washington-head-quarter-dollar-coin.png'))
        else:
            await ctx.send(embed=makeembed('Coin Flip', 'Tails', discord.Color.green(), 'https://www.nicepng.com/png/full/146-1464848_quarter-tail-png-tails-on-a-coin.png'))
    
    #roll a die
    @commands.command(name='roll', aliases=['dice'])
    async def roll(self, ctx):
        dice = random.randint(1,6)
        await ctx.send(embed=makeembed('Rolling Dice', f'You rolled a {dice}', discord.Color.green(), 'https://www.nicepng.com/png/full/393-3932479_white-dice-png.png'))
    
    # rock paper scissors
    @commands.command(name='rpsls', aliases=['rps'])
    async def rpsls(self, ctx):
        choices = ['rock', 'paper', 'scissors']
        choice = random.choice(choices)
        await ctx.send(embed=makeembed('Rock Paper Scissors', f'You chose {choice}', discord.Color.green(), None))

    # guess the number
    @commands.command(name='guess', aliases=['number'])
    async def guess(self, ctx, number):
        if number.isdigit():
            if int(number) == random.randint(1,100):
                await ctx.send(embed=makeembed('Guess the Number', 'Correct!', discord.Color.green(), None))
            else:
                await ctx.send(embed=makeembed('Guess the Number', 'Incorrect!', discord.Color.red(), None))
        else:
            await ctx.send(embed=makeembed('Guess the Number', 'Invalid number', discord.Color.red(), None))




def setup(commands):
    commands.add_cog(tictactoe(commands))
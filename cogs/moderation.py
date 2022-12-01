# *********************************#
#   Moderation commands           #
#                                 #
#   These should only be          #
#   available to server admins &  #
#   mods!                         #
# *********************************#
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from datetime import datetime
from lib.working_with_json import *

# check for warnings.json file
create_json_if_not_exists('JSON/warnings.json')

# check for bans.json file
create_json_if_not_exists('JSON/bans.json')

# check for poll.json file
create_json_if_not_exists('JSON/poll.json')


# Get current time and date
def get_time():
    return datetime.now().strftime('%m/%d/%y %I:%M:%S %p')


# make embed
def make_embed(color, name, value):
    embed = discord.Embed(color=color)
    embed.add_field(name=name, value=value)
    return embed


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands!')

    # enable / disable slowmode for x seconds
    @app_commands.command(name='slowmode', description='Enable or disable slowmode.')
    @commands.has_role('new role1')
    async def slowmode(self, interaction: discord.Interaction, seconds: int) -> None:
        await interaction.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await interaction.response.send_message(embed=make_embed(
                discord.Color.green(), 'Success', 'Slowmode has been disabled!'))
        await interaction.response.send_message(embed=make_embed(
            discord.Color.green(), 'Success', f'Slowmode set to {seconds} seconds!'))

    # give warning
    @app_commands.command(name='warn', description='Give warning to a member.')
    @commands.has_role('new role1')
    async def warn(self, interaction: discord.Interaction, username: discord.Member, reason: str = None):

        load_warnings = load_json('JSON/warnings.json')

        if str(username.id) not in load_json('JSON/warnings.json'):
            load_warnings[username.id] = []
            load_warnings[username.id].append({
                'warned_by': interaction.user.id,
                'time': get_time(),
                'reason': reason
            })
            # save to json
            save_json(load_warnings, 'JSON/warnings.json')
            await interaction.response.send_message(
                embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been warned'))
        else:
            # add warning to user
            load_warnings[str(username.id)].append({
                'warned_by': interaction.user.id,
                'time': get_time(),
                'reason': reason
            })
            # save to json
            save_json(load_warnings, 'JSON/warnings.json')

            await interaction.response.send_message(
                embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been warned'))

    # list warnings
    @app_commands.command(name='listwarnings', description='List the warnings for a members.')
    @commands.has_role('new role1')
    async def listwarnings(self, interaction: discord.Interaction, username: discord.Member):
        load_warnings = load_json('JSON/warnings.json')
        if str(username.id) not in load_warnings:
            await interaction.response.send_message(f'{username.name} has no warnings')
        else:
            embed = discord.Embed(
                title=f'{username.name} warnings', color=discord.Color.red())
            for warning in load_warnings[str(username.id)]:
                embed.add_field(name=warning['time'],
                                value=f'Warned by {self.bot.get_user(int(warning["warned_by"])).name}'
                                      f'\nReason: {warning["reason"]}',
                                inline=False)
                embed.set_thumbnail(url=username.avatar)
            await interaction.response.send_message(embed=embed)

    # kick member
    @app_commands.command(name='kick', description='Kick a member from the server.')
    @commands.has_role('new role1')
    async def kick(self, interaction: discord.Interaction, username: discord.Member, reason: str):
        await username.kick(reason=reason)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Kick Success', f'{username.name} has been kicked!'))

    # ban member
    @app_commands.command(name='ban', description='Ban a member from the server.')
    @commands.has_role('new role1')
    async def ban(self, interaction: discord.Interaction, username: discord.Member, reason: str = None):
        await username.ban(reason=reason)
        msg = await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Ban Succsess', f'{username.name} has been banned!'))

    # remove only messages from a specific user
    @app_commands.command(name='purgeuser', description='Purger messages from one user.')
    @commands.has_role('new role1')
    async def purgeuser(self, interaction: discord.Interaction, username: discord.Member, number: int = 10):
        print(number)
        await interaction.response.defer()
        await interaction.channel.purge(limit=number + 1, check=lambda m: m.author == username)
        await interaction.followup.send(
            embed=make_embed(discord.Color.green(), 'Success', f'✅ Messages from {username.name} has been removed!'))

    # mute member
    @app_commands.command(name='mute', description='Mute a member.')
    @commands.has_role('new role1')
    async def mute(self, interaction: discord.Interaction, username: discord.Member, *, reason: str = None):
        # create muted role if it doesn't exist
        if not discord.utils.get(interaction.guild.roles, name='muted'):
            muted_role = await interaction.guild.create_role(name='muted')
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        role = discord.utils.get(interaction.guild.roles, name='muted')
        await username.add_roles(role)
        embed = discord.Embed()
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been muted!'))

    # temp mute member
    @app_commands.command(name='tempmute', description='Temporarily mute a member.')
    @commands.has_role('new role1')
    async def tempmute(self, interaction: discord.Interaction, username: discord.Member, time: int, reason: str = None):
        role = discord.utils.get(interaction.guild.roles, name='muted')
        await username.add_roles(role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been muted for {time} seconds!'))
        await asyncio.sleep(time)
        await username.remove_roles(role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been unmuted!'))

    # unmute member
    @app_commands.command(name='unmute', description='Unmute a member.')
    @commands.has_role('new role1')
    async def unmute(self, interaction: discord.Interaction, username: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name='muted')
        await username.remove_roles(role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'{username.name} has been unmuted!'))

    # unban member
    @app_commands.command(name='unban', description='Unban a member.')
    @commands.has_role('new role1')
    async def unban(self, interaction: discord.Interaction, *, username: str):
        banned_users = await interaction.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            await interaction.guild.unban(user)
            await interaction.response.send_message(
                embed=make_embed(discord.Color.green(), 'Success', f'✅ {user} has been unbanned!'))

    # change nickname
    @app_commands.command(name='nickname', description='Change members nickname.')
    @commands.has_role('new role1')
    async def nickname(self, interaction: discord.Interaction, username: discord.Member, nickname: str):
        await username.edit(nick=nickname)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success',
                             f'{username.name} nickname has been changed to {nickname}'))

    # remove nickname
    @app_commands.command(name='removenickname', description='Remove members nickname.')
    @commands.has_role('new role1')
    async def removenickname(self, interaction: discord.Interaction, username: discord.Member):
        await username.edit(nick=None)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'{username.name} nickname has been removed'))

    # remove all warnings from member
    @app_commands.command(name='clearallwarnings', description='Clear all warning for a member')
    @commands.has_role('new role1')
    async def clearallwarnings(self, interaction: discord.Interaction, username: discord.Member):
        load_warnings = load_json('JSON/warnings.json')
        if str(username.id) not in load_warnings:
            await interaction.response.send_message(f'{username.name} has no warnings')
        else:
            del load_warnings[str(username.id)]
            save_json(load_warnings, 'JSON/warnings.json')
            await interaction.response.send_message(f'{username.name} warnings have been cleared')

    # remove the last warning from member. If last warning then remove the user from the list
    @app_commands.command(name='clearlastwarning', description='Clears the last givin warning for a member.')
    @commands.has_role('new role1')
    async def clearlastwarning(self, interaction: discord.Interaction, username: discord.Member):
        load_warnings = load_json('JSON/warnings.json')
        if str(username.id) not in load_warnings:
            await interaction.response.send_message(
                embed=make_embed(discord.Color.red(), 'Error', f'{username.name} has no warnings'))
        else:
            if len(load_warnings[str(username.id)]) == 1:
                del load_warnings[str(username.id)]
                save_json(load_warnings, 'JSON/warnings.json')
                await interaction.response.send_message(embed=make_embed(discord.Color.green(), 'Success',
                                                                         f'{username.name} '
                                                                         f'last warning has been cleared!'))
            else:
                load_warnings[str(username.id)].pop()
                save_json(load_warnings, 'JSON/warnings.json')
                await interaction.response.send_message(embed=make_embed(discord.Color.green(), 'Success',
                                                                         f'{username.name} last warning has been cleared!'))

    # remove a specific warning from member
    # todo create a better ux; list warnings and select one using a button
    @app_commands.command(name='clearwarning', description='Remove a specific warning using its index')
    @commands.has_role('new role1')
    async def clearwarning(self, interaction: discord.Interaction, username: discord.Member, warning: int = None):
        load_warnings = load_json('JSON/warnings.json')
        if str(username.id) not in load_warnings:
            await interaction.response.send_message(
                embed=make_embed(discord.Color.red(), 'Error', f'{username.name} has no warnings'))
        else:
            if not warning:
                embed = discord.Embed(
                    title=f'What warning would you like to remove?', color=discord.Color.red())
                for index, warning in enumerate(load_warnings[str(username.id)]):
                    index += 1
                    embed.add_field(name=warning['time'],
                                    value=f'Index: {index} \n Warned by {self.bot.get_user(int(warning["warned_by"])).name}\nReason: {warning["note"]}',
                                    inline=False)
                embed.set_thumbnail(url=username.avatar)
                embed.set_footer(text='Example: .clearwarning @user 1')
                await interaction.response.send_message(embed=embed)
            else:
                try:
                    load_warnings[str(username.id)].pop(warning - 1)
                    save_json(load_warnings, 'JSON/warnings.json')
                    await interaction.response.send_message(embed=make_embed(discord.Color.green(), 'Success',
                                                                             f'{username.name} warning {warning} has been cleared!'))
                except IndexError:
                    await interaction.response.send_message(embed=make_embed(discord.Color.red(), 'Error',
                                                                             f'{username.name} warning {warning} does not exist'))

    # purge messages
    @app_commands.command(name='purge', description='Purge x amount of messages.')
    @commands.has_role('new role1')
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        msg = await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'✅ {amount} messages have been purged!'))
        await asyncio.sleep(3)
        await msg.delete()

    # show infomation about a member
    @app_commands.command(name='userinfo', description='Display infomation about a member.')
    @commands.has_role('new role1')
    async def userinfo(self, interaction: discord.Interaction, username: discord.Member):
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name='Username', value=username.name)
        embed.add_field(name='ID', value=username.id)
        embed.add_field(name='Nickname', value=username.nick)
        embed.add_field(name='Status', value=username.status)
        embed.add_field(name='Joined At', value=username.joined_at)
        embed.add_field(name='Created At', value=username.created_at)
        embed.add_field(name='Top Role', value=username.top_role)
        if username.avatar:
            embed.set_thumbnail(url=username.avatar)
        else:
            embed.set_thumbnail(url=username.default_avatar)
        embed.set_footer(
            text=f'Requested by {interaction.user.name}', icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    # create poll
    # todo https://github.com/JohnnyJayJay/instant-poll/blob/main/poll-demo.gif
    # @app_commands.command(name='poll', description='Create a poll.')
    # @commands.has_role('new role1')
    # async def poll(self, interaction: discord.Interaction, question: str):
    #
    #     # check if a poll in poll.json has the status of 'open'
    #     # if it does, then the bot will not create another poll
    #     # if it doesn't, then the bot will create a new poll
    #
    #     def make_poll(question):
    #         embed = discord.Embed(title='Poll', color=discord.Color.green())
    #         embed.add_field(name='Question', value=question)
    #         view = View()
    #         option1 = Button(style=discord.ButtonStyle.blurple, emoji="✅")
    #         option2 = Button(style=discord.ButtonStyle.green, emoji="❌")
    #         view.add_item(option1)
    #         view.add_item(option2)
    #         return [view, embed]
    #
    #     get_polls = load_json('JSON/poll.json')
    #     msg = await interaction.response.send_message(view=make_poll(question)[0], embed=make_poll(question)[1])
    #
    #     try:
    #         latest_poll_id = get_polls['latestPollID']
    #     except KeyError:
    #         latest_poll_id = 0
    #
    #     if len(get_polls) == 0:
    #         get_polls['latestPollID'] = msg.id
    #         get_polls[msg.id] = [{
    #             'question': question,
    #             'status': 'open',
    #             'reactions': [],
    #             'author': interaction.user.id,
    #             'channel': interaction.channel.id
    #         }]
    #         save_json(get_polls, 'JSON/poll.json')
    #         # await msg.add_reaction('✅')
    #         # await msg.add_reaction('❌')
    #
    #     elif get_polls[str(latest_poll_id)][0]['status'] == 'o pen':
    #         await msg.delete()
    #         await interaction.response.send_message(
    #             embed=make_embed(discord.Color.red(), 'Error', 'A poll is already open!'))
    #     else:
    #         get_polls['latestPollID'] = msg.id
    #         get_polls[msg.id] = [{
    #             'question': question,
    #             'status': 'open',
    #             'reactions': [],
    #             'author': interaction.user.id,
    #             'channel': interaction.channel.id
    #         }]
    #         save_json(get_polls, 'JSON/poll.json')
    #         await msg.add_reaction('✅')
    #         await msg.add_reaction('❌')
    #
    # # close poll and get total number of checks and crosses
    # @app_commands.command(name='closepoll', description='Close the current open poll.')
    # @commands.has_role('new role1')
    # async def closepoll(self, interaction: discord.Interaction):
    #     get_polls = load_json('JSON/poll.json')
    #
    #     try:
    #         latest_poll_id = load_json('JSON/poll.json')['latestPollID']
    #     except KeyError:
    #         latest_poll_id = 0
    #
    #     if len(load_json('JSON/poll.json')) == 0:
    #         await interaction.response.send_message(
    #             embed=make_embed(discord.Color.red(), 'Error', 'There is no poll to close!'))
    #     elif get_polls[str(latest_poll_id)][0]['status'] == 'closed':
    #         await interaction.response.send_message(
    #             embed=make_embed(discord.Color.red(), 'Error', 'There is no poll to close!'))
    #     else:
    #         get_polls[str(latest_poll_id)][0]['status'] = 'closed'
    #         print(get_polls)
    #         save_json(get_polls, 'JSON/poll.json')
    #
    #         # get total number of checks and crosses
    #         get_poll = await interaction.fetch_message(latest_poll_id)
    #
    #         for reaction in get_poll.reactions:
    #             if reaction.emoji == '✅':
    #                 checks = reaction.count - 1
    #             elif reaction.emoji == '❌':
    #                 crosses = reaction.count - 1
    #
    #         emebed = discord.Embed(title='Poll Results',
    #                                color=discord.Color.green())
    #         emebed.add_field(name='Question', value=get_polls[str(
    #             latest_poll_id)][0]['question'], inline=False)
    #         emebed.add_field(name='✅', value=checks)
    #         emebed.add_field(name='❌', value=crosses)
    #         emebed.add_field(name='Total', value=checks + crosses)
    #         emebed.set_footer(text=f'Here is a jump link for the poll')
    #         await ctx.send(embed=emebed)

    # say something
    @app_commands.command(name='say', description='Say something.')
    @commands.has_role('new role1')
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    # add role
    @app_commands.command(name='addrole', description='Add a roll to a member.')
    @commands.has_role('new role1')
    async def addrole(self, interaction: discord.Interaction, username: discord.Member, role: str):
        role = discord.utils.get(interaction.guild.roles, name=role)
        await username.add_roles(role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Success', f'✅ {role} has been added to {username.name}'))

    # remove role
    @app_commands.command(name='removerole', description='Remove a roll from a member.')
    @commands.has_role('new role1')
    async def removerole(self, interaction: discord.Interaction, username: discord.Member, role: str):
        role = discord.utils.get(interaction.guild.roles, name=role)
        await username.remove_roles(role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.red(), 'Role Removed', f'{role} has been removed from {username.name}'))

    # create new role
    @app_commands.command(name='createrole', description='Create a server roll.')
    @commands.has_role('new role1')
    async def createrole(self, interaction: discord.Interaction, role: str):
        await interaction.guild.create_role(name=role)
        await interaction.response.send_message(
            embed=make_embed(discord.Color.green(), 'Role Created', f'{role} has been created'))

    # delete role from server
    @commands.command(name='deleterole')
    @commands.has_role('new role1')
    async def deleterole(self, ctx, *, role):
        role = discord.utils.get(ctx.guild.roles, name=role)
        await role.delete()
        await ctx.send(embed=make_embed(discord.Color.red(), 'Role Deleted', f'{role} has been deleted'))

    # create new text or voice channel
    @app_commands.command(name='createchannel', description='Create a text/voice channel.')
    @commands.has_role('new role1')
    async def createchannel(self, interaction: discord.Interaction, channel_type: str, channel: str):
        channel_type = channel_type.lower()
        if channel_type == 'text':
            await interaction.guild.create_text_channel(channel)
            await interaction.response.send_message(
                embed=make_embed(discord.Color.green(), 'Channel Created', f'{channel} has been created'))
        elif channel_type == 'voice':
            await interaction.guild.create_voice_channel(channel)
            await interaction.response.send_message(
                embed=make_embed(discord.Color.green(), 'Channel Created', f'{channel} has been created'))
        else:
            await interaction.response.send_message(
                embed=make_embed(discord.Color.red(), 'Error', 'Please enter a valid type'))

    # delete channel
    @commands.command(name='deletechannel')
    @commands.has_role('new role1')
    async def deletechannel(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.channels, name=channel)
        print(channel)
        await channel.delete()
        await ctx.send(embed=make_embed(discord.Color.red(), 'Channel Deleted', f'{channel} has been deleted'))

    # list channels
    @commands.command(name='listchannels')
    @commands.has_role('new role1')
    async def listchannels(self, ctx):
        for channel in ctx.guild.channels:
            await ctx.send(f'{channel}')

    # lock channel
    @commands.command(name='lockchannel')
    @commands.has_role('new role1')
    async def lockchannel(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.channels, name=channel)
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(embed=make_embed(discord.Color.green(), 'Channel Locked', f'{channel} has been locked'))

    # unlock channel
    @commands.command(name='unlockchannel')
    @commands.has_role('new role1')
    async def unlockchannel(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.channels, name=channel)
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(embed=make_embed(discord.Color.green(), 'Channel Unlocked', f'{channel} has been unlocked'))


async def setup(bot):
    await bot.add_cog(Moderation(bot), guilds=[discord.Object(id=911372583235092480)])

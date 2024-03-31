import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from lib.working_with_json import *
import traceback


def create_progress_bar(yes_votes, total_votes):
    try:
        barfill = (100 * (yes_votes / total_votes)) / 2
        percent = 100 * (yes_votes / total_votes)
    except ZeroDivisionError:
        barfill = 0
        percent = 0
    bar = "█" * int(barfill) + " " * (50 - int(barfill))
    return f"|{bar}| {percent:.2f}%"


class SlashTest(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll", description="This is a test for polls")
    async def poll(
        self,
        interaction: discord.Interaction,
        question: str,
        a: str,
        b: str,
        c: str = None,
    ):
        bars = []
        interactions = []
        options = [a, b, c]
        buttons = {}
        totals = {}
        view = View()
        for i in enumerate(options):
            if i[1] is not None:
                # set a button1-x to a button object with the label of a poll option
                buttons["button{0}".format(i[0])] = Button(label=i[1])

                # button callback that sends back the poll option
                async def button_callback(interaction, o=i[1]):
                    data = load_json("JSON/poll.json")
                    # store the interaction to a json file
                    if interaction.user.name not in data:
                        updict = {interaction.user.name: [{"selection": o}]}
                        updict.update(data)
                        save_json(updict, "JSON/poll.json")
                        data = load_json("JSON/poll.json")
                        if "total" not in data:
                            totals[o] = 1
                            data["total"] = [totals]
                            save_json(data, "JSON/poll.json")
                        elif "total" in data:
                            if o in data["total"][0]:
                                add_one = data["total"][0][o] + 1
                                data["total"][0][o] = add_one
                                save_json(data, "JSON/poll.json")
                            elif o not in data["total"]:
                                dic = data["total"][0]
                                dic[o] = 1
                                data["total"] = [dic]
                                save_json(data, "JSON/poll.json")

                    elif interaction.user.name in data:
                        past_selection = data[interaction.user.name][0]["selection"]
                        past_selection_current_total = data["total"][0][past_selection]
                        if past_selection != o:
                            data[interaction.user.name][0]["selection"] = o
                            if o not in data["total"][0]:
                                data["total"][0][o] = 1
                                past_selection_new_toal = (
                                    past_selection_current_total - 1
                                )
                                data["total"][0][
                                    past_selection
                                ] = past_selection_new_toal
                            elif o in data["total"][0]:
                                current_total = data["total"][0][o]
                                data["total"][0][o] = current_total + 1
                                past_selection_new_toal = (
                                    past_selection_current_total - 1
                                )
                                data["total"][0][
                                    past_selection
                                ] = past_selection_new_toal

                            save_json(data, "JSON/poll.json")
                    try:
                        current_total = sum(data["total"][0].values())
                        for bar in bars:
                            try:
                                bar[1] = create_progress_bar(
                                    data["total"][0][bar[0]], current_total
                                )
                            except KeyError:
                                bar[1] = create_progress_bar(0, current_total)
                        response = "{}\n\n```".format(question)
                        for bar in bars:
                            response += "{} {}\n".format(bar[0], bar[1])

                        response += f"```\n You can pick one\nNumber of participants: {current_total}"
                        print(bars)
                        await interaction.response.edit_message(content=response)
                    except:
                        traceback.print_exc()

                # store the callback in a list
                interactions.append(button_callback)

                # store the bars in a list
                bars.append([i[1], create_progress_bar(0, 1)])

        for button in enumerate(buttons):
            # add the button to the view
            view.add_item(buttons[button[1]])
            # assian each button to its repective callback
            buttons[button[1]].callback = interactions[button[0]]

        async def close_poll(interaction):
            try:
                await interaction.response.edit_message(
                    content=f"{interaction.message.content}\n Poll has been closed by {interaction.user.name}"
                )

            except:
                traceback.print_exc()

        close_poll_button = Button(label="Close Poll")
        view.add_item(close_poll_button)
        close_poll_button.callback = close_poll

        response = "{}\n\n```".format(question)
        for bar in bars:
            response += "{} {}\n".format(bar[0], bar[1])

        response += "```\n You can pick one\n Number of participants: 0"

        await interaction.response.send_message(response, view=view)


async def setup(bot):
    await bot.add_cog(SlashTest(bot), guilds=[discord.Object(id=911372583235092480)])

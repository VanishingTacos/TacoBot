"""
https://github.com/alphascriptyt/Discord_Rewrite_Tutorials/blob/master/episodes/episode-16.py
This is compressed into one file.
"""

import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from StringProgressBar import progressBar
import datetime
import time

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))

        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

        global starttime
        starttime = datetime.datetime.utcnow()

        global duration
        duration = pafy.new(song).duration

    async def converttoseconds(self, time):
        seconds = (sum([a*b for a,b in zip([3600, 60, 1], map(int, time.split(":")))]) - 1)
        return seconds
       

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            try:
                queue_len = len(self.song_queue[ctx.guild.id])
            except:
                queue_len = 0

            if queue_len < 10:
                try:
                    self.song_queue[ctx.guild.id].append(song)
                except:
                    self.song_queue[ctx.guild.id] = [song]
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        song_name = pafy.new(song).title
        embed = discord.Embed(title="Now Playing", description=song_name, color=0x00ff00)
        embed.add_field(name="Duration", value=pafy.new(song).duration)
        embed.add_field(name="Likes", value=pafy.new(song).likes)
        embed.add_field(name="Views", value=pafy.new(song).viewcount)
        embed.add_field(name="Uploader", value=pafy.new(song).author)
        embed.add_field(name="URL", value = '[Click here](%s)' % song)
        embed.set_thumbnail(url=pafy.new(song).thumb)
        await ctx.send(embed=embed)

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        options = []
        song_info = []
        for entry in info["entries"]:
             options.append(discord.SelectOption(label=entry["title"]))
             song_info.append([entry["title"], entry["webpage_url"]])
        select = Select(placeholder="Pick a song",options=options)
        
        async def my_callback(interaction):
            for i in song_info:
                if i[0] == select.values[0]:
                    url = i[1]
            if ctx.voice_client.source is not None:
                try:
                    queue_len = len(self.song_queue[ctx.guild.id])
                except:
                    queue_len = 0

                if queue_len < 10:
                    try:
                        self.song_queue[ctx.guild.id].append(url)
                    except:
                        self.song_queue[ctx.guild.id] = [url]
                    return await interaction.response.send_message(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

                else:
                    return await interaction.response.send_message("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")
            else:
                await interaction.response.defer(ephemeral = True)
                start = time.time()
                await self.play_song(ctx, url)
                video_to_pafy = pafy.new(url)
                title = video_to_pafy.title
                embed = discord.Embed(title="Now Playing", description=title, color=0x00ff00)
                embed.add_field(name="Duration", value=video_to_pafy.duration)
                embed.add_field(name="Likes", value= video_to_pafy.likes)
                embed.add_field(name="Views", value= video_to_pafy.viewcount)
                embed.add_field(name="Uploader", value= video_to_pafy.author)
                embed.add_field(name="URL", value = '[Click here](%s)' % url)
                embed.set_thumbnail(url= video_to_pafy.thumb)
                end = time.time()
                print(end - start)
                await interaction.followup.send(embed=embed)
                print('debug')

        select.callback = my_callback
        view = View()
        view.add_item(select)

        await ctx.send(view=view)

        
    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(15) # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.red())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()

    #stop the bot from playing music
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.voice_client.source is not None:
            ctx.voice_client.stop()
            return await ctx.send("Stopping the current song.")
        else:
            return await ctx.send("I am not currently playing any songs.")
    
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")
        
        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")
    
    #get the name of the song that is currently playing
    @commands.command()
    async def nowplaying(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if ctx.voice_client.source is None:
            return await ctx.send("I am not currently playing any song.")

        await ctx.send(f"Now playing: {ctx.voice_client.source.title}")

    # volume command
    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if volume < 0 or volume > 100:
            return await ctx.send("Volume must be between 0 and 100.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Volume set to {volume}%.")

    # view the current volume
    @commands.command()
    async def  volumeview(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        await ctx.send(f"The current volume is {ctx.voice_client.source.volume * 100}%.")

    # progress of the song
    @commands.command()
    async def progress(self, ctx):
        if ctx.voice_client.source is None:
            return await ctx.send("I am not playing any song.")
        uptime = datetime.datetime.utcnow() - starttime
        time = str(uptime).split(".")[0]
        timeseconds = await self.converttoseconds(time)
        durationseconds = await self.converttoseconds(duration)
        bardata = progressBar.splitBar(int(durationseconds), int(timeseconds), size=20)
        embed = discord.Embed(title="Progress", description=f"{time} {bardata[0]} {duration}", colour=discord.Colour.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))
    
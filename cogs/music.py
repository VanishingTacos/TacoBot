# discord cog to play music, add music to queue, skip, pause, resume, etc.
import discord
from discord.ext import commands
import youtube_dl
import os
import json

# check for queue.json
if not os.path.exists('./JSON/queue.json'):
    with open('./JSON/queue.json', 'w') as f:
        json.dump({}, f)

#function to load queue.json
def _loadQueue():
    with open('./JSON/queue.json', 'r') as f:
        return json.load(f)

# function for saving to queue.json
def saveQueue(queue):
    with open('./JSON/queue.json', 'w') as f:
        json.dump(queue, f)

FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
YDL_OPTIONS = {'format': 'bestaudio'}

get = discord.utils.get

class music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='connect')
    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel.')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(name='disconnect')
    async def disconnect(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('I am not in a voice channel.')
    

    @commands.command(name='play', aliases=['queue'])
    async def play(self, ctx, *, url):
        vc = ctx.voice_client
        # add url to queue.json
        queue = _loadQueue()
        # check if queue.json is empty
        if len(queue) == 0:
            queue[str(ctx.author.id)] = [url]
            saveQueue(queue)
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                # get title
                title = info['title'] 
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                vc.play(source)
        else:
            # check if user is in queue.json
            if str(ctx.author.id) in queue:
                queue[str(ctx.author.id)].append(url)
                saveQueue(queue)
                await ctx.send('Added to queue.')
                
            else:
                queue[str(ctx.author.id)] = [url]
                saveQueue(queue)
                await ctx.send('Added to queue.')
        
    
    # remove url from queue.json and play next url
    @commands.command(name='skip')
    async def skip(self, ctx):
        vc = ctx.voice_client
        queue = _loadQueue()
        # check if queue.json is empty
        if len(queue) == 0:
            await ctx.send('Queue is empty.')
        else:
            # check if user is in queue.json
            if str(ctx.author.id) in queue:
                # check if user is playing
                if vc.is_playing():
                    # skip song
                    vc.stop()
                    # remove url from queue.json
                    del queue[str(ctx.author.id)][0]
                    saveQueue(queue)
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(queue[str(ctx.author.id)][0], download=False)
                        # get title
                        title = info['title'] 
                        url2 = info['formats'][0]['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                        vc.play(source)
                        await ctx.send('Skipped.')
                else:
                    # remove url from queue.json
                    del queue[str(ctx.author.id)][0]
                    saveQueue(queue)                    
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(queue[str(ctx.author.id)][0], download=False)
                        # get title
                        title = info['title'] 
                        url2 = info['formats'][0]['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                        vc.play(source)
                        await ctx.send('Skipped.')
            else:
                await ctx.send('You are not in the queue.')

    # clear queue.json
    @commands.command(name='clearqueue')
    async def clearqueue(self, ctx):
        queue = _loadQueue()
        # check if queue.json is empty
        if len(queue) == 0:
            await ctx.send('Queue is empty.')
        else:
            # check if user is in queue.json
            if str(ctx.author.id) in queue:
                # remove url from queue.json
                queue.pop(str(ctx.author.id))
                saveQueue(queue)
                await ctx.send('Queue cleared.')
            else:
                await ctx.send('You are not in the queue.')

    
    @commands.command(name='pause')
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not in a voice channel.')
        else:
            ctx.voice_client.pause()
            await ctx.send('Paused ⏸')
    
    @commands.command(name='resume')
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not in a voice channel.')
        else:
            ctx.voice_client.resume()
            await ctx.send('Resumed ▶')
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('I am not in a voice channel.')
        else:
            ctx.voice_client.stop()
            await ctx.send('Stopped ⏹')


def setup(bot):
    bot.add_cog(music(bot))
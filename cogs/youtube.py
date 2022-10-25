from pprint import pprint
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import urllib.request, urllib.parse
import json
import os
from pprint import pprint

load_dotenv()

# check for youtube_users.json
if not os.path.exists('./JSON/youtube_users.json'):
    with open('./JSON/youtube_users.json', 'w') as f:
        json.dump({}, f)

#load youtube_users.json
with open('./JSON/youtube_users.json', 'r') as f:
    youtube_users = json.load(f)

# load youtube_users.json function
def load_youtube():
    with open('./JSON/youtube_users.json', 'r') as f:
        return json.load(f)

# function for saving to youtube_users.json
def save_youtube(youtube):
    with open('./JSON/youtube_users.json', 'w') as f:
        json.dump(youtube, f)



api_key = os.environ.get("YOUTUBE_API_KEY")
base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
base_channel_url = 'https://www.googleapis.com/youtube/v3/channels?'


def get_channel_id(username):
    search_url = base_search_url+'q={}&type=channel&maxResults=1&key={}'.format(username, api_key)
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)

    channel_id = resp['items'][0]['id']['channelId']
    return channel_id

def get_channel_profile_image(channel_id):
    search_url = base_channel_url + 'part=snippet&id={}&fields=items/snippet/thumbnails&key={}'.format(channel_id, api_key)
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)

    channel_profile_image = resp['items'][0]['snippet']['thumbnails']['medium']['url']
    return channel_profile_image
    
def get_newest_video_in_channel(channel_id):
    search_url = base_search_url+'channelId={}&order=date&part=id&type=video&maxResults=1&key={}'.format(channel_id, api_key)
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)

    newest_video_id = resp['items'][0]['id']['videoId']
    return newest_video_id


def create_embed(title, userid, viewer_count, get_user_profile_pic):
    embed = discord.Embed(title = title, url = f"https://twitch.tv/{userid}")
    embed.add_field(name = "Viewers", value = viewer_count)
    embed.set_author(name = userid, icon_url = get_user_profile_pic)
    embed.set_image(url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{userid}-320x180.jpg")
    embed.set_thumbnail(url = get_user_profile_pic)
    return embed




class youtube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes = 15)
    async def new_video_notifs_loop(self):
        username = urllib.parse.quote("Devon Stuper")
        if len(load_youtube()) == 0:
            channel_id = get_channel_id(username)
            profile_image = get_channel_profile_image(channel_id)
            newest_video = get_newest_video_in_channel(channel_id)
            username = urllib.parse.unquote(username)
            youtube_users[username] = []
            youtube_users[username].append({
                'newest_video': newest_video,
                'channel_id': channel_id,
                'profile_image': profile_image
                
            })
            save_youtube(youtube_users)

    @commands.Cog.listener()
    async def on_ready(self):
        self.new_video_notifs_loop.start()


async def setup(bot):
    await bot.add_cog(youtube(bot))
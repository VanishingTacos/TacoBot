import json
from tabnanny import check
from turtle import width
import discord
from discord.ext import commands, tasks
from matplotlib.image import thumbnail
from matplotlib.pyplot import get
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv
import requests
from pprint import pprint
import traceback

load_dotenv()

# check for stream_state.json
if not os.path.exists('./JSON/stream_state.json'):
    with open('./JSON/stream_state.json', 'w') as f:
        json.dump({}, f)

#load stream_state.json
with open('./JSON/stream_state.json', 'r') as f:
    stream_state = json.load(f)

# load stream_state.json function
def load_stream_state():
    with open('./JSON/stream_state.json', 'r') as f:
        return json.load(f)

# function for saving to stream_state.json
def save_stream_state(stream_state):
    with open('./JSON/stream_state.json', 'w') as f:
        json.dump(stream_state, f)

def create_embed(title, userid, viewer_count, get_user_profile_pic):
    embed = discord.Embed(title = title, url = f"https://twitch.tv/{userid}")
    embed.add_field(name = "Viewers", value = viewer_count)
    embed.set_author(name = userid, icon_url = get_user_profile_pic)
    embed.set_image(url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{userid}-320x180.jpg")
    embed.set_thumbnail(url = get_user_profile_pic)
    return embed


# Authentication with Twitch API.
client_id =  os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_ENDPOINT = "https://api.twitch.tv/helix/streams?user_login="
TWITCH_USER_ENDPOINT = "https://api.twitch.tv/helix/users?login="
body = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()

API_HEADERS = {
    'Client-ID': client_id, 
    'Authorization': 'Bearer ' + keys['access_token'], 
    'Accept': 'application/vnd.twitchtv.v5+json'
}



# Returns true if online, false if not.
def checkuser(userid):
    # Get Twitch user infomation
    get_user_url = TWITCH_USER_ENDPOINT + userid
    get_user_req = requests.Session().get(get_user_url, headers=API_HEADERS)
    get_user_json = get_user_req.json()
    get_user_profile_pic = get_user_json['data'][0]['profile_image_url']
    # Get Twitch stream data
    get_stream_url = TWITCH_STREAM_ENDPOINT + userid
    get_stream_req = requests.Session().get(get_stream_url, headers=API_HEADERS)
    get_stream_json = get_stream_req.json()
    if get_stream_json['data']:
        title = get_stream_json['data'][0]['title']
        game_name = get_stream_json['data'][0]['game_name']
        viewer_count = get_stream_json['data'][0]['viewer_count']
        if userid not in load_stream_state():
            stream_state[userid] = []
            stream_state[userid].append({
                'is_live': True,
                'title': title,
                'game_name': game_name

                })
            save_stream_state(stream_state)
            return create_embed(title, userid, viewer_count, get_user_profile_pic)
        elif userid in load_stream_state():
            if stream_state[userid][0]['is_live'] == True:
                return True
            elif stream_state[userid][0]['is_live'] == False:
                stream_state[userid][0]['is_live'] = True
                title = get_stream_json['data'][0]['title']
                stream_state[userid][0]['title'] = title
                stream_state[userid][0]['game_name'] = game_name
                viewer_count = get_stream_json['data'][0]['viewer_count']
                save_stream_state(stream_state)
                return create_embed(title, userid, viewer_count, get_user_profile_pic)
    else:
        if userid not in load_stream_state():
            stream_state[userid] = []
            stream_state[userid].append({
                'is_live': False,
                'title': None,
                'game_name': None

            })
            save_stream_state(stream_state)
        elif userid in load_stream_state():
            if stream_state[userid][0]['is_live'] == True:
                stream_state[userid][0]['is_live'] = False
                save_stream_state(stream_state)
            return False



class twitch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def live_notifs_loop(self):
        get_embed = checkuser('vanishingtacos')
        print(get_embed)

        if not get_embed:
            pass
        else:
            try:
                await self.bot.get_channel(911372583235092485).send(embed = get_embed)
            except:
                pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.live_notifs_loop.start()


async def setup(bot):
    await bot.add_cog(twitch(bot))
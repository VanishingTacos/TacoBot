import discord
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch
from dotenv import load_dotenv
import requests
from lib.working_with_json import *
from pprint import pprint as pp

load_dotenv()

base_dir = os.environ.get("BASE_DIR")

# check for stream_state.json
create_json_if_not_exists(base_dir, 'JSON/stream_state.json')


def create_embed(title, userid, viewer_count, get_user_profile_pic):
    embed = discord.Embed(title=title, url=f"https://twitch.tv/{userid}")
    embed.add_field(name="Viewers", value=viewer_count)
    embed.set_author(name=userid, icon_url=get_user_profile_pic)
    embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{userid}-320x180.jpg")
    embed.set_thumbnail(url=get_user_profile_pic)
    return embed


# Authentication with Twitch API.
client_id = os.environ.get("TWITCH_CLIENT_ID")
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
print(keys)

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
    get_user_display_name = get_user_json['data'][0]['display_name']
    # Get Twitch stream data
    get_stream_url = TWITCH_STREAM_ENDPOINT + userid
    get_stream_req = requests.Session().get(get_stream_url, headers=API_HEADERS)
    get_stream_json = get_stream_req.json()
    if get_stream_json['data']:
        # load stream_state.json
        stream_state = load_json('JSON/stream_state.json')
        title = get_stream_json['data'][0]['title']
        game_name = get_stream_json['data'][0]['game_name']
        viewer_count = get_stream_json['data'][0]['viewer_count']
        if userid not in stream_state:
            stream_state[userid] = []
            stream_state[userid].append({
                'is_live': True,
                'title': title,
                'game_name': game_name

            })
            save_json(stream_state, 'JSON/stream_state.json')
            return create_embed(title, get_user_display_name, viewer_count, get_user_profile_pic), get_user_display_name
        elif userid in load_json('JSON/stream_state.json'):
            stream_state = load_json('JSON/stream_state.json')
            if stream_state[userid][0]['is_live']:
                return True
            elif not load_json('JSON/stream_state.json')[userid][0]['is_live']:
                stream_state = load_json('JSON/stream_state.json')
                stream_state[userid][0]['is_live'] = True
                title = get_stream_json['data'][0]['title']
                stream_state[userid][0]['title'] = title
                stream_state[userid][0]['game_name'] = game_name
                viewer_count = get_stream_json['data'][0]['viewer_count']
                save_json(stream_state, 'JSON/stream_state.json')
                return create_embed(title, get_user_display_name, viewer_count,
                                    get_user_profile_pic), get_user_display_name
    else:
        if userid not in load_json('JSON/stream_state.json'):
            # load stream_state.json
            stream_state = load_json('JSON/stream_state.json')
            stream_state[userid] = []
            stream_state[userid].append({
                'is_live': False,
                'title': None,
                'game_name': None

            })
            save_json(stream_state, 'JSON/stream_state.json')
        elif userid in load_json('JSON/stream_state.json'):
            # load stream_state.json
            stream_state = load_json('JSON/stream_state.json')
            if stream_state[userid][0]['is_live']:
                stream_state[userid][0]['is_live'] = False
                save_json(stream_state, 'JSON/stream_state.json')
            return False


class Twitch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def live_notifs_loop(self):
        name = 'tayxo'
        check = checkuser(name)

        try:
            await self.bot.get_channel(911372583235092485).send(
                f"{check[1]} is now live on https://twitch.tv/{name}! Go check it out!", embed=check[0])
        except AttributeError:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        self.live_notifs_loop.start()


async def setup(bot):
    await bot.add_cog(Twitch(bot))

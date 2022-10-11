import json
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()

# Authentication with Twitch API.
client_id =  os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?"
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
    'Accept': 'application/vnd.twitchtv.v5+json'}

# Returns true if online, false if not.
def checkuser(userid):
    userid = twitch.get_users(logins=[userid])['data'][0]['id']
    url = TWITCH_STREAM_API_ENDPOINT_V5 + "user_id=" + userid
    try:
        req = requests.Session().get(url, headers=API_HEADERS)
        jsondata = req.json()
        if jsondata['data']:
             return jsondata
        else:
            return False
    except Exception as e:
        print("Error checking user: ", e)
        return False
    except IndexError:
        return False


class twitchtest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        print(checkuser(""))
    
    live_notifs_loop.start()


async def setup(bot):
    await bot.add_cog(twitchtest(bot))
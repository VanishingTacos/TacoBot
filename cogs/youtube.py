import urllib.parse
import urllib.request
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import traceback
from pprint import pprint

from lib.working_with_json import *

load_dotenv()

# check for youtube_users.json
create_json_if_not_exists("JSON/youtube_users.json")

api_key = os.environ.get("YOUTUBE_API_KEY")
base_search_url = "https://www.googleapis.com/youtube/v3/search?"
base_channel_url = "https://www.googleapis.com/youtube/v3/channels?"
base_videos_url = "https://www.googleapis.com/youtube/v3/videos?"


def get_channel_id(username):
    username = urllib.parse.quote(username)
    search_url = base_search_url + "q={}&type=channel&maxResults=1&key={}".format(
        username, api_key
    )
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)

    channel_id = resp["items"][0]["id"]["channelId"]
    return channel_id


def get_channel_profile_image(channel_id):
    search_url = (
        base_channel_url
        + "part=snippet&id={}&fields=items/snippet/thumbnails&key={}".format(
            channel_id, api_key
        )
    )
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)

    channel_profile_image = resp["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
    return channel_profile_image


def get_newest_video_in_channel(channel_id):
    search_url = (
        base_search_url
        + "channelId={}&order=date&part=id&type=video&maxResults=1&key={}".format(
            channel_id, api_key
        )
    )
    inp = urllib.request.urlopen(search_url)
    resp = json.load(inp)
    newest_video_id = resp["items"][0]["id"]["videoId"]

    video_url = base_videos_url + "part=snippet&id={}&key={}".format(
        newest_video_id, api_key
    )
    inp = urllib.request.urlopen(video_url)
    resp = json.load(inp)

    newest_video_thumbnail = resp["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
    newest_video_title = resp["items"][0]["snippet"]["title"]

    return newest_video_id, newest_video_thumbnail, newest_video_title


def create_embed(title, userid, get_user_profile_pic, videoid):
    embed = discord.Embed(title=title, url=f"https://www.youtube.com/watch?v={videoid}")
    embed.set_author(name=userid, icon_url=get_user_profile_pic)
    embed.set_image(url=f"https://img.youtube.com/vi/{videoid}/0.jpg")
    return embed


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=15)
    async def new_video_notifs_loop(self):
        # load youtube_users.json function
        load_youtube = load_json("JSON/youtube_users.json")
        username = "###"
        if username in load_youtube:
            channel_id = load_youtube[username][0]["channel_id"]
            profile_image = get_channel_profile_image(channel_id)

            newest_video_tuple = get_newest_video_in_channel(channel_id)
            newest_video = newest_video_tuple[0]
            newest_video_title = newest_video_tuple[2]

            if profile_image != load_youtube[username][0]["profile_image"]:
                load_youtube[username][0]["profile_image"] = profile_image

            if newest_video != load_youtube[username][0]["newest_video"]:
                load_youtube[username][0]["newest_video"] = newest_video
                embed = create_embed(
                    newest_video_title,
                    username,
                    load_youtube[username][0]["profile_image"],
                    newest_video,
                )

            await self.bot.get_channel(911372583235092485).send(
                f"Hey! {username} has a new video on YouTube! Go check it out!",
                embed=embed,
            )

            save_json(load_youtube, "JSON/youtube_users.json")
        elif username not in load_youtube:
            channel_id = get_channel_id(username)
            profile_image = get_channel_profile_image(channel_id)
            newest_video = get_newest_video_in_channel(channel_id)
            load_youtube[username] = []
            load_youtube[username].append(
                {
                    "newest_video": newest_video,
                    "channel_id": channel_id,
                    "profile_image": profile_image,
                }
            )
            save_json(load_youtube, "JSON/youtube_users.json")

    @commands.Cog.listener()
    async def on_ready(self):
        self.new_video_notifs_loop.start()


async def setup(bot):
    await bot.add_cog(Youtube(bot))

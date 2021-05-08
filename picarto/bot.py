from discord.ext import commands
from discord import Embed

from .channel_embed import get_big_embed, get_minimal_embed

import requests

from .models.channelDetails import ChannelDetails


def get_channel_data(channel_name: str) -> ChannelDetails:
    uri = f"https://api.picarto.tv/api/v1/channel/name/{channel_name}"
    headers = {
        "User-Agent": "somebot"
    }

    response = requests.get(uri, headers=headers)

    data = response.json()
    details = ChannelDetails.parse_obj(data)

    return details


class Picarto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.group()
    async def picarto(self, ctx: commands.Context):
        pass

    @picarto.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("picarto pong")

    @picarto.command()
    async def check(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Check if channel is live, with minimal extra info

        details = get_channel_data(name)
        embed = get_minimal_embed(details)

        await ctx.send(embed=embed)

    @picarto.command()
    async def info(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all information about a channel

        details = get_channel_data(name)
        embed = get_big_embed(details)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Picarto(bot))

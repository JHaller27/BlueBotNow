from discord.ext import commands
from requests.models import Response

from .channel_embed import get_big_embed, get_minimal_embed

import os
import requests

from .models.channelDetails import ChannelDetails


class CallerError(RuntimeError):
    def __init__(self, response: Response, *args: object) -> None:
        super().__init__(str(response))
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def ux_message(self) -> str:
        return f"Failed call: {self.status_code}"

    @property
    def full_message(self) -> str:
        text = 'Requires capta' if 'meta name="captcha-bypass"' in self.text else self.text

        return f"Failed call with code: {self.status_code}.\n" + text


def get_channel_data(channel_name: str) -> ChannelDetails:
    host = os.environ.get('PICARTO_HOST') or 'https://api.picarto.tv/api/v1'

    uri = f"{host}/channel/name/{channel_name}"
    headers = {
        "User-Agent": "curl/7.68.0"
    }

    response = requests.get(uri, headers=headers)

    if response.status_code != 200:
        raise CallerError(response)

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

        try:
            details = get_channel_data(name)
            embed = get_minimal_embed(details)

            await ctx.send(embed=embed)

        except CallerError as err:
            print(err.full_message)
            await ctx.send(err.ux_message)

    @picarto.command()
    async def info(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all information about a channel

        try:
            details = get_channel_data(name)
            embed = get_big_embed(details)

            await ctx.send(embed=embed)

        except CallerError as err:
            print(err.full_message)
            await ctx.send(err.ux_message)


def setup(bot):
    bot.add_cog(Picarto(bot))

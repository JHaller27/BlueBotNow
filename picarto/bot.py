from typing import Union

from discord.ext import commands
from discord import Embed

from datetime import datetime, timedelta

import requests

from .models.channelDetails import ChannelDetails


PICARTO_GREEN = 0x1DA557
OFFLINE = 0x4F545C


def get_channel_data(channel_name: str) -> ChannelDetails:
    uri = f"https://api.picarto.tv/api/v1/channel/name/{channel_name}"
    headers = {
        "User-Agent": "somebot"
    }

    response = requests.get(uri, headers=headers)

    data = response.json()
    details = ChannelDetails.parse_obj(data)

    return details


def format_label(value: int, one_label: str, many_label: str) -> str:
    assert value > 0

    if value == 1:
        return f'{value} {one_label}'

    return f'{value} {many_label}'


def format_delta(delta: timedelta) -> str:
    time = int(delta.total_seconds())

    if time < 1:
        return '<1 second'

    if time < 60:
        return format_label(time, 'second', 'seconds')

    time = time // 60
    if time < 60:
        return format_label(time, 'minute', 'minutes')

    time = time // 60
    if time < 60:
        return format_label(time, 'hour', 'hours')

    time //= 24
    if time < 24:
        return format_label(time, 'day', 'days')

    time //= 30
    if time < 30:
        return format_label(time, 'month', 'months')

    time //= 12
    return format_label(time, 'year', 'years')


def get_offline_message(details: ChannelDetails) -> Union[str, int]:
    last_seen = datetime.strptime(details.last_live, r'%Y-%m-%d %H:%M:%S')
    now = datetime.utcnow()
    delta = now - last_seen
    ago_msg = format_delta(delta)

    return f'_{details.name}_ is currently **offline**.\n' + \
           f'They were last online _{ago_msg} ago_.', OFFLINE


def get_online_message(details: ChannelDetails) -> Union[str, int]:
    return f'_{details.name}_ is currently **online**!\n' + \
           f'Watch them at https://www.picarto.tv/{details.name}.', PICARTO_GREEN


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
        details = get_channel_data(name)

        if details.online:
            msg, color = get_online_message(details)
        else:
            msg, color = get_offline_message(details)

        embed = Embed(
            title=f"{details.name} on Picarto.tv",
            url=f"https://www.picarto.tv/{details.name}",
            description=msg,
            color=color,
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Picarto(bot))

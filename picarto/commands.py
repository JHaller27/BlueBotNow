from discord.ext import commands
from utils.logging import Logger
from commands import CustomCommand

from caller import get_channel_data
from .channel_embed import get_big_embed, get_status_badge


class Check(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "check", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)

        await self.ctx.send(get_status_badge(details))


class Info(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "info", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)
        embed = get_big_embed(details)

        await self.ctx.send(embed=embed)

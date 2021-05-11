from discord.ext import commands
from utils.logging import Logger
from commands import CustomCommand

from caller import get_channel_data
from .channel_embed import get_minimal_embed


class Check(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "check", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name)
        embed = get_minimal_embed(details)

        await self.ctx.send(embed=embed)
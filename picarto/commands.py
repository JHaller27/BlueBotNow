from discord.ext import commands
from utils.logging import Logger
from commands import CustomCommand
from discord import Embed
from caller import get_channel_data
from .channel_embed import ChannelEmbedMeta, get_big_embed


class Check(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "check", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)
        meta = ChannelEmbedMeta(details)

        embed = Embed(title=meta.title, url=meta.url)

        if img := meta.thumbnail:
            embed.set_thumbnail(url=img)
        if meta.online:
            if img := meta.image:
                embed.set_image(url=img)

        embed.color = meta.color

        await self.ctx.send(embed=embed)


class Info(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "info", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)
        embed = get_big_embed(details)

        await self.ctx.send(embed=embed)


class Rules(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "rules", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)
        
        meta = ChannelEmbedMeta(details)
        embed = Embed(title=meta.title, url=meta.url)
        
        name, value = meta.rules_panel
        embed.add_field(name=name, value=value, inline=False)

        await self.ctx.send(embed=embed)


class Links(CustomCommand):
    def __init__(self, logger: Logger, ctx: commands.Context):
        super().__init__("picarto", "links", logger, ctx)

    async def _run(self, *args):
        (name, ) = args

        details = get_channel_data(name, self._logger)
        
        meta = ChannelEmbedMeta(details)
        embed = Embed(title=meta.title, url=meta.url)

        name, value = meta.links_panel
        embed.add_field(name=name, value=value, inline=False)

        await self.ctx.send(embed=embed)

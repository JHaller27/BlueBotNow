from .models.channelDetails import ChannelDetails
from discord import Embed

from datetime import datetime

from utils.formatting import format_delta


# region AbstractsAndInterfaces

class CheckEmbedBuilder:
    def can_handle(self, details: ChannelDetails) -> bool:
        raise NotImplementedError

    def build(self, details: ChannelDetails) -> Embed:
        raise NotImplementedError


class CheckEmbedDecorator(CheckEmbedBuilder):
    _base: CheckEmbedBuilder

    def __init__(self, base: CheckEmbedBuilder) -> None:
        super().__init__()
        self._base = base

    @property
    def base(self) -> CheckEmbedBuilder:
        return self._base

    def build(self, details: ChannelDetails) -> Embed:
        embed = self.base.build(details)

        if self.can_handle(details):
            self.decorate_embed(details, embed)

        return embed

    def can_handle(self, details: ChannelDetails) -> bool:
        raise NotImplementedError

    def decorate_embed(self, details: ChannelDetails, embed: Embed):
        raise NotImplementedError

# endregion AbstractsAndInterfaces


class CheckEmbedBase(CheckEmbedBuilder):
    def can_handle(self, details: ChannelDetails) -> bool:
        return True

    def build(self, details: ChannelDetails) -> Embed:
        # This is the default Embed
        # All default options go here
        return Embed(
            title=f"{details.name} on Picarto.tv",
            url=f"https://www.picarto.tv/{details.name}",
        )


#region Decorators

class OnlineDecorator(CheckEmbedDecorator):
    PICARTO_GREEN_COLOR = 0x1DA557

    def __init__(self, base: CheckEmbedBuilder):
        super().__init__(base)

    def can_handle(self, details: ChannelDetails) -> bool:
        return details.online

    def decorate_embed(self, details: ChannelDetails, embed: Embed):
        embed.description = f'_{details.name}_ is currently **online**!\n' + \
            f'Watch them at https://www.picarto.tv/{details.name}.'
        embed.color = OnlineDecorator.PICARTO_GREEN_COLOR


class OfflineDecorator(CheckEmbedDecorator):
    OFFLINE_COLOR = 0x4F545C

    def __init__(self, base: CheckEmbedBuilder):
        super().__init__(base)

    def can_handle(self, details: ChannelDetails) -> bool:
        return not details.online

    def decorate_embed(self, details: ChannelDetails, embed: Embed):
        last_seen = datetime.strptime(details.last_live, r'%Y-%m-%d %H:%M:%S')
        now = datetime.utcnow()
        delta = now - last_seen
        ago_msg = format_delta(delta)

        embed.description = f'_{details.name}_ is currently **offline**.\n' + \
            f'They were last online _{ago_msg} ago_.'
        embed.color = OfflineDecorator.OFFLINE_COLOR


# Add more decorators here by copying the __init__, and implementing can_handle() and decorate_embed().
# Then add new decorator to factory() below

# endregion Decorators


def factory(details: ChannelDetails) -> Embed:
    builder = CheckEmbedBase()
    builder = OnlineDecorator(builder)
    builder = OfflineDecorator(builder)

    return builder.build(details)

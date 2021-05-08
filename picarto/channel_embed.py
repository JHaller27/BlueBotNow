from typing import Optional

from .models.channelDetails import ChannelDetails
from discord import Embed
from datetime import datetime
from itertools import islice

from utils.formatting import format_delta, format_list_text


class ChannelEmbedMeta:
    PICARTO_GREEN_COLOR = 0x1DA557
    OFFLINE_COLOR = 0x4F545C

    def __init__(self, details: ChannelDetails):
        self._channel_details = details

    @property
    def online(self) -> bool:
        return self._channel_details.online or False

    @property
    def title(self) -> str:
        details = self._channel_details

        if details.title is None or details.title == '':
            return f'{details.name} on Picarto.tv'

        return f'{details.name} - {details.title}'

    @property
    def url(self) -> str:
        return f"https://www.picarto.tv/{self._channel_details.name}"

    @property
    def description(self) -> str:
        # If channel is online...
        if self.online:
            online_text = f'_{self._channel_details.name}_ is currently **online**'

            # If channel is a multistream, add each stream participant
            if len(self._channel_details.multistream) > 0:
                with_list = format_list_text([ms.name for ms in self._channel_details.multistream])
                online_text += f' with {with_list}'

            return f'{online_text}!\n' + \
                   f'Watch them at https://www.picarto.tv/{self._channel_details.name}.'

        # If channel is offline, show how long since they were last online
        last_seen = datetime.strptime(self._channel_details.last_live, r'%Y-%m-%d %H:%M:%S')
        now = datetime.utcnow()
        delta = now - last_seen
        ago_msg = format_delta(delta)

        return f'_{self._channel_details.name}_ is currently **offline**.\n' + \
            f'They were last online _{ago_msg} ago_.'

    @property
    def color(self) -> int:
        return self.PICARTO_GREEN_COLOR if self.online else self.OFFLINE_COLOR

    @property
    def tags(self) -> Optional[str]:
        if len(self._channel_details.tags) == 0:
            return None

        return ':label: ' + ', '.join(self._channel_details.tags)

    @property
    def nsfw(self) -> Optional[str]:
        if not self._channel_details.adult:
            return None

        return ':warning: NSFW'

    @property
    def gaming(self) -> Optional[str]:
        if not self._channel_details.gaming:
            return None

        return ':video_game: Gaming'

    @property
    def thumbnail(self) -> Optional[str]:
        return self._channel_details.avatar

    @property
    def image(self) -> Optional[str]:
        return self._channel_details.thumbnails.tablet

    @property
    def languages(self) -> Optional[str]:
        if len(self._channel_details.languages) == 0:
            return None

        return format_list_text(self._channel_details.languages)

    @property
    def panels(self) -> list[tuple[str, str]]:
        for idx, panel in enumerate(sorted(self._channel_details.description_panels, key=lambda p: p.position)):
            title = panel.title
            if title is None or title == '':
                title = f"Panel {idx+1}"
            yield (title, panel.body)


def get_minimal_embed(details: ChannelDetails) -> Embed:
    meta = ChannelEmbedMeta(details)

    embed = Embed(title=meta.title, url=meta.url)
    embed.description = meta.description

    if img := meta.thumbnail:
        embed.set_thumbnail(url=img)
    if meta.online:
        if img := meta.image:
            embed.set_image(url=img)

    for name, value in islice(meta.panels, 1):
        embed.add_field(name=name, value=value, inline=False)

    return embed


def get_big_embed(details: ChannelDetails) -> Embed:
    # Placeholder - will more info add later
    return get_minimal_embed(details)

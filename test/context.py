from .guild import Guild
from .author import Author


class Context:
    # Simplest possible Context mock. Add properties as needed.
    # Official documentation for reference: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?#context

    @property
    def guild(self) -> Guild:
        return Guild()

    @property
    def author(self) -> Author:
        return Author()

    async def send(self, content = None, *, embed = None, **kwargs):
        # Instead of sending to Discord, send to the stdin!
        if content:
            print(f"content={content}")
        if embed:
            print_embed(embed)
        if kwargs and len(kwargs) > 0:
            print(f"kwargs={kwargs}")


def print_embed(embed):
    sep = "\n" + "-" * 40

    embed_dict = embed.to_dict()

    print("Embed")
    if title := embed_dict.get('title'):
        print("\tTitle:", title)
    if url := embed_dict.get('url'):
        print("\tUrl:", url)
    if color := embed_dict.get('color'):
        print("\tColor:", color)
    if thumbnail := embed_dict.get('thumbnail'):
        print("\tThumbnail Url:", thumbnail.get('url'))
    if fields := embed_dict.get('fields'):
        print("\tFields:")
        for panel in fields:
            print("\t\tInline:", panel.get('inline'))
            print("\t\tName:", panel.get('name'))
            print("\t\tValue:", sep)
            print(panel.get('value'), sep)
    if description := embed_dict.get('description'):
        print("\tDescription:", sep)
        print(description, sep)

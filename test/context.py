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
    print("\tTitle:", embed_dict['title'])
    print("\tUrl:", embed_dict['url'])
    print("\tColor:", embed_dict['color'])
    print("\tThumbnail Url:", embed_dict['thumbnail']['url'])
    print("\tDescription:", embed_dict['description'])
    print("\tFields:")
    for panel in embed_dict['fields']:
        print("\t\tInline:", panel['inline'])
        print("\t\tName:", panel['name'])
        print("\t\tValue:", sep)
        print(panel['value'], sep)
    print("\tDescription:", sep)
    print(embed_dict['description'], sep)

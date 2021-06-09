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
            print(f"embed={embed.to_dict()}")
        if kwargs and len(kwargs) > 0:
            print(f"kwargs={kwargs}")

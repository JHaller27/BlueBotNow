from discord.ext import commands
from discord import Embed
from requests.models import Response

from .models.posts import Posts
from .models.post import Post

import os
import requests


E621_COLOR = 0x152F56
NO_RESULTS_COLOR = 0x4F545C


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
        return f"Failed call with code: {self.status_code}.\n" + self.text


def get_posts(tags: list[str], limit: int = 5) -> list[Post]:
    host = os.environ.get('E621_HOST') or 'https://e621.net'

    tag_list = '+'.join(tags)
    uri = f"{host}/posts.json?limit={limit}&tags={tag_list}"
    headers = {
        "User-Agent": "BlueBotNow/1.0 by Wizinja27"
    }

    response = requests.get(uri, headers=headers)

    if response.status_code != 200:
        raise CallerError(response)

    data = response.json()
    posts_obj = Posts.parse_obj(data)

    return posts_obj.posts


class E621(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.group()
    async def e621(self, ctx: commands.Context):
        pass

    @e621.command()
    async def search(self, ctx: commands.Context, *tags: str):
        limit = 1
        tag_query = '+'.join(tags)

        try:
            posts = get_posts(tags, limit)
            embed = Embed(title="Search e621.net", url=f'https://e621.net/posts?tags={tag_query}')

            if len(posts) == 0:
                embed.description = "No results for: " + ", ".join(tags)
                embed.color = NO_RESULTS_COLOR

                await ctx.send(embed=embed)
                return

            p: Post = posts[0]

            embed.set_thumbnail(url=p.preview.url)
            embed.add_field(name="Tags", value=":label: " + ", ".join(tags))
            embed.color = E621_COLOR

            await ctx.send(embed=embed)

        except CallerError as err:
            print(err.full_message)
            await ctx.send(err.ux_message)


def setup(bot):
    bot.add_cog(E621(bot))

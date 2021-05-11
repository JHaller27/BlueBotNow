from picarto.commands import Check
from utils.logging import Logger

from discord.ext import commands

from .channel_embed import get_big_embed
from caller import get_channel_data, CallerError


class Picarto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.group()
    async def picarto(self, ctx: commands.Context):
        Logger("picarto").info(ctx.author.name, "invoked a picarto command")

    @picarto.command()
    async def check(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Check if channel is live, with minimal extra info
        cmd = Check(Logger("picarto"), ctx)
        await cmd.run(name)

    @picarto.command()
    async def info(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all information about a channel

        Logger("picarto").debug(f"enter info({name})")

        try:
            details = get_channel_data(name)
            embed = get_big_embed(details)

            await ctx.send(embed=embed)

        except CallerError as err:
            print(err.full_message)
            await ctx.send(err.ux_message)

        finally:
            Logger("picarto").debug(f"exit info({name})")


def setup(bot):
    bot.add_cog(Picarto(bot))

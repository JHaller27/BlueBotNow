from picarto.commands import Check, Info, Rules, Links
from utils.logging import Logger

from discord.ext import commands


class Picarto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._logger = Logger("picarto")

    @commands.group()
    async def picarto(self, ctx: commands.Context):
        pass

    @picarto.command()
    async def check(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Check if channel is live, with minimal extra info
        cmd = Check(self._logger, ctx)
        await cmd.run(name)

    @picarto.command()
    async def info(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all information about a channel
        cmd = Info(self._logger, ctx)
        await cmd.run(name)
        
    @picarto.command()
    async def rules(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all the rules listed in the channel
        cmd = Rules(self._logger, ctx)
        await cmd.run(name)
        
    @picarto.command()
    async def links(self, ctx: commands.Context, name: str = 'BGNlive'):
        # Get all the affiliated links tied to the channel
        cmd = Links(self._logger, ctx)
        await cmd.run(name)


def setup(bot):
    bot.add_cog(Picarto(bot))

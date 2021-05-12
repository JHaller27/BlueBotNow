from caller import CallerError
from discord.ext import commands

from utils.logging import Logger
from utils.tools import short_hash


class CustomCommand:
    def __init__(self, bot_name: str, cmd_name: str, logger: Logger, ctx: commands.Context):
        self._bot_name = bot_name
        self._cmd_name = cmd_name
        self._logger = logger
        self._ctx = ctx

    @property
    def id(self) -> int:
        return short_hash(
            self._ctx.guild.id,
            self._ctx.author.id,
            id(self)
        )

    @property
    def name(self) -> str:
        return f"{self._bot_name}.{self._cmd_name}"

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def ctx(self) -> commands.Context:
        return self._ctx

    async def _run(self, *args):
        raise NotImplementedError

    async def run(self, *args):
        args_str = ','.join(args)
        self.logger.info(f"Invoking {self.name}({args_str}) (id: {self.id})")
        self.logger.debug(f"{self.id} invoked for user {self.ctx.author.id} ({self.ctx.author.name}) in guild {self.ctx.guild.id} ({self.ctx.guild.name})")

        try:
            await self._run(*args)
        except CallerError as err:
            print(err.full_message)
            await self.ctx.send(err.ux_message)

        self.logger.debug(f"{self.id} invocation finished")

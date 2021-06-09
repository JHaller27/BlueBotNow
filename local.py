from bot import bot
from test.context import Context
from picarto.cog import Picarto
import asyncio


ctx = Context()

picarto = Picarto(bot)
asyncio.run(picarto.info(picarto, ctx))

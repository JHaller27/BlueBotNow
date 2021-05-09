from utils.tools import read_env, read_secret
import utils.logging as logging

from discord.ext import commands


# Set up logging
logging.set_level(logging.Level.INFO)
logger = logging.Logger("root")


class Bot(commands.Bot):
    async def on_ready(self):
        logger.info(f"Bot is ready using prefix '{self.command_prefix}'")


bot = Bot(command_prefix=read_env('DISCORD_PREFIX', '/'))


def extend(bot, name: str, logger: logging.Logger):
    logger.debug(f"Loading extension {name}")
    bot.load_extension(name)
    logger.debug(f"Finished loading extension {name}")


extend(bot, 'picarto.bot', logger)
extend(bot, 'e621.bot', logger)

try:
    bot_token = read_secret('DISCORD_TOKEN')

    logger.debug("Token:", bot_token)

    # Run Bot
    bot.run(bot_token.value)

except ValueError:
    logger.error("Discord token not found. Failed to start bot.")
    logger.warn("Go to https://discord.com/developers/applications/840469974983245844/bot + authenticate to retrieve token")

finally:
    logger.debug("Shutting down bot")

from utils.tools import read_env, read_secret
import utils.logging as logging

from discord.ext import commands


# Set up logging
logging.set_level(read_env('LOG_LEVEL', 'INFO'))
logger = logging.Logger("root")

logger.debug("Log level:", logging.level)


class Bot(commands.Bot):
    async def on_ready(self):
        logger.info(f"Bot is ready using prefix '{self.command_prefix}'")
        for guild in self.guilds:
            logger.info(f"Connected to guild {guild.id} {guild.name}")


bot = Bot(command_prefix=read_env('DISCORD_PREFIX', '/', logger=logger))


def extend(bot, name: str, logger: logging.Logger):
    logger.debug(f"Loading extension {name}")
    bot.load_extension(name)
    logger.debug(f"Finished loading extension {name}")


extend(bot, 'picarto.cog', logger)
extend(bot, 'e621.cog', logger)


# Only run these if this file is run directly
if __name__ == "__main__":
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

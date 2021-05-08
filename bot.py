import os
import sys
from discord.ext import commands


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Bot is ready using prefix '{self.command_prefix}'")


prefix = os.environ.get('DISCORD_PREFIX') or '/'
bot = Bot(command_prefix=prefix)
bot.load_extension('picarto.bot')

# Run Bot
token_env_name = 'DISCORD_TOKEN'
bot_token = os.environ.get(token_env_name)
if bot_token is None:
    print(f"'{token_env_name}' not found in environment. Failed to start bot.", file=sys.stderr)
    print(f"Go to https://discord.com/developers/applications/840469974983245844/bot + authenticate to retrieve token")
    sys.exit(1)
print(f"'Token: {bot_token}'")
bot.run(bot_token)

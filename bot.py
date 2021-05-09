import os
import sys
from utils.formatting import Secret
from discord.ext import commands


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Bot is ready using prefix '{self.command_prefix}'")


prefix = os.environ.get('DISCORD_PREFIX') or '/'
bot = Bot(command_prefix=prefix)
bot.load_extension('picarto.bot')
bot.load_extension('e621.bot')

# Run Bot
token_env_name = 'DISCORD_TOKEN'
bot_token = Secret(os.environ.get(token_env_name))

if bot_token.is_empty:
    print(f"'{token_env_name}' not found in environment. Failed to start bot.", file=sys.stderr)
    print(f"Go to https://discord.com/developers/applications/840469974983245844/bot + authenticate to retrieve token")
    sys.exit(1)

print("Token:", bot_token)
bot.run(bot_token.value)

from utils.tools import read_env, read_secret

from discord.ext import commands


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Bot is ready using prefix '{self.command_prefix}'")


bot = Bot(command_prefix=read_env('DISCORD_PREFIX', '/'))

bot.load_extension('picarto.bot')
bot.load_extension('e621.bot')

bot_token = read_secret('DISCORD_TOKEN',
    err_msg="'{0}' not found in environment. Failed to start bot.\n" + \
        "Go to https://discord.com/developers/applications/840469974983245844/bot + authenticate to retrieve token",
)
print("Token:", bot_token)

# Run Bot
bot.run(bot_token.value)

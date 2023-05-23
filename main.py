from libraries import bot
import os

if __name__ == '__main__':
    bot.run_discord_bot(token=os.getenv('BOT_TOKEN'))

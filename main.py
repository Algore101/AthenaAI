from libraries import bot
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.txt')

if __name__ == '__main__':
    # Import settings
    settings = {}
    with open(SETTINGS_FILE, 'r') as file:
        for line in file:
            line = line.strip()
            settings[line.split('=')[0]] = line.split('=')[1]
    bot.run_discord_bot(token=os.getenv('BOT_TOKEN'), prefix=settings['prefix'])

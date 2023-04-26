import discord
import responses
import datetime

ALT_COMMANDS = {
    'hero': 'all',
    'dps': 'damage',
    'healer': 'support',
    'user': 'profile',
}

HERO_COMMANDS = ['tank', 'damage', 'support', 'all']


async def send_message(message, response, is_private=False):
    if 'direct message' in str(message.channel).lower():
        await message.author.send(response) if is_private else await message.channel.send(response)
    else:
        await message.author.send(response) \
            if is_private else await message.channel.send(response, reference=message)


def run_discord_bot():
    token = 'MTA5MjgzNDIyNjAxNTA0MzU5NA.GeYcHm.-BpyujKd4fOuOKvlaUTDINi8qPqNlolqqzNP74'
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user_message = str(message.content).lower()
        if len(message.content) == 0:
            return
        if message.content[0] != '.':
            return

        username = str(message.author)
        channel = str(message.channel)
        command = user_message.split(' ')[0][1:]
        argument = ''
        for word in user_message.split(' ')[1:]:
            argument += f'{word} '
        argument = argument.strip()

        print(f'[{datetime.datetime.now()}] {username}: "{user_message}" ({channel})')
        # Convert alt commands
        if command in ALT_COMMANDS:
            command = ALT_COMMANDS[command]
        # Run commands
        if command in HERO_COMMANDS:
            # Return random hero from selected category.
            if argument == '':
                await send_message(message, responses.choose_hero(username, command))
            elif argument.lower() == 'duo':
                await send_message(message, responses.choose_duo(username, command, False))
            elif argument.lower() == 'rduo':
                await send_message(message, responses.choose_duo(username, command))
            return
        elif command == 'dm':
            # Respond to the message
            if 'direct message' not in str(message.channel).lower():
                await send_message(message, responses.greet_privately()[0])
            # Send a private message to the user.
            await send_message(message, responses.greet_privately()[1], is_private=True)
            return
        elif command == 'help':
            # Send a help message
            await send_message(message, responses.help_menu())
            return
        elif command == 'profile':
            # Send information of user profile
            await send_message(message, responses.get_profile(username))
            return
        elif command == 'avoid':
            # Add hero to avoid list
            await send_message(message, responses.avoid_hero(username, argument))
            return
        elif command == 'unavoid':
            # Remove hero from avoid list
            await send_message(message, responses.unavoid_hero(username, argument))
            return
        elif command == 'duo':
            response = 'Please try using `duo` as an argument.\n' \
                      'E.g. `.support duo` for supports that work well together\n' \
                      'Tip: also try using `rduo` as an argument for two random heroes.'
            await send_message(message, response)
        elif command == 'role':
            await send_message(message, responses.choose_role())

    client.run(token)

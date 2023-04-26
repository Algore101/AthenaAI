import discord
import responses
import datetime
import os

ALT_COMMANDS = {
    'hero': 'all',
    'dps': 'damage',
    'healer': 'support',
    'user': 'profile',
}
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'discord_token.txt')
DISCORD_TOKEN = open(TOKEN_FILE, 'r').read()


async def send_message(message, response, is_private=False):
    if 'direct message' in str(message.channel).lower():
        await message.author.send(response) if is_private else await message.channel.send(response)
    else:
        await message.author.send(response) \
            if is_private else await message.channel.send(response, reference=message)


async def _process_command(command, **kwargs) -> list:
    reply = []
    category_args = {'duo': False, 'rduo': True}
    commands = {
        'tank': responses.choose_duo if kwargs['duo'] in list(category_args.keys()) else responses.choose_hero,
        'damage': responses.choose_duo if kwargs['duo'] in list(category_args.keys()) else responses.choose_hero,
        'support': responses.choose_duo if kwargs['duo'] in list(category_args.keys()) else responses.choose_hero,
        'all': responses.choose_duo if kwargs['duo'] in list(category_args.keys()) else responses.choose_hero,
        'dm': responses.greet_privately,
        'help': responses.help_menu,
        'profile': responses.get_profile,
        'avoid': responses.avoid_hero,
        'unavoid': responses.unavoid_hero,
        'role': responses.choose_role,
        'duo': responses.duo,
        'rduo': responses.rduo,
    }
    try:
        # Set category for hero commands
        if command in ['tank', 'damage', 'support', 'all']:
            kwargs['category'] = command
            # Set duo type
            if kwargs['duo'] in list(category_args.keys()):
                kwargs['random_duo'] = category_args[kwargs['duo']]
                del kwargs['duo']
        if command != 'dm':
            reply.append(commands[command](**kwargs))
        else:
            reply += commands[command](**kwargs)
        return reply
    except KeyError:
        return reply


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
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
        # Process commands
        reply = await _process_command(
            command, username=username, duo=argument, hero_to_avoid=argument, hero_to_unavoid=argument
        )
        if command != 'dm':
            try:
                await send_message(message, reply[0])
            except IndexError:
                pass
        else:
            # Respond to the message
            if 'direct message' not in str(message.channel).lower():
                await send_message(message, reply[0])
            # Send a private message to the user.
            await send_message(message, reply[1], is_private=True)

    client.run(DISCORD_TOKEN)

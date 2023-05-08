import asyncio
import discord
from libraries import responses, profiles
import datetime

ALT_COMMANDS = {
    'hero': 'all',
    'dps': 'damage',
    'healer': 'support',
    'user': 'profile',
    'score': 'scores',
    'scoreboard': 'scores',
    'leaderboard': 'scores',
}
TRIVIA_EMOJIS = ["🇦", "🇧", "🇨", "🇩"]


async def send_message(context: discord.Message, response, is_private=False) -> discord.Message:
    if type(response) == discord.Embed:
        embed = response
        content = None
    else:
        content = response
        embed = None

    if is_private:
        return await context.author.send(content=content, embed=embed)
    else:
        # Reply to server message
        if 'direct message' not in str(context.channel).lower():
            return await context.channel.send(content=content, embed=embed, reference=context)
        else:
            return await context.channel.send(content=content, embed=embed)


async def _process_command(command, argument, username, prefix) -> list:
    kwargs = {'username': username, 'prefix': prefix}
    reply = []
    category_args = {'duo': False, 'rduo': True}
    commands = {
        'tank': responses.choose_duo if argument in list(category_args.keys()) else responses.choose_hero,
        'damage': responses.choose_duo if argument in list(category_args.keys()) else responses.choose_hero,
        'support': responses.choose_duo if argument in list(category_args.keys()) else responses.choose_hero,
        'all': responses.choose_duo if argument in list(category_args.keys()) else responses.choose_hero,
        'dm': responses.greet_privately,
        'help': responses.help_menu,
        'profile': responses.get_profile,
        'avoid': responses.avoid_hero,
        'unavoid': responses.unavoid_hero,
        'role': responses.choose_role,
        'duo': responses.duo,
        'rduo': responses.rduo,
        'list': responses.get_heroes_in_category,
        'trivia': responses.get_trivia_question,
        'guess': responses.get_trivia_image,
        'scores': responses.get_scoreboard,
    }
    try:
        # Set arguments
        if command in ['tank', 'damage', 'support', 'all']:
            kwargs['category'] = command
            # Set duo type
            if argument in list(category_args.keys()):
                kwargs['random_duo'] = category_args[argument]
        elif command == 'list':
            if argument in ALT_COMMANDS:
                argument = ALT_COMMANDS[argument]
            kwargs['category'] = argument
        elif command == 'avoid':
            kwargs['hero_to_avoid'] = argument
        elif command == 'unavoid':
            kwargs['hero_to_unavoid'] = argument
        elif command == 'trivia':
            kwargs['number_of_questions'] = argument
        elif command == 'guess':
            kwargs['difficulty'] = argument

        # Build reply
        if command != 'dm':
            reply.append(commands[command](**kwargs))
        else:
            reply += commands[command](**kwargs)
        return reply
    except KeyError:
        return reply


async def _send_trivia_questions(bot: discord.Client, context: discord.Message, reply: list):
    total_questions = 0
    successful_questions = 0
    if type(reply[0]) is str:
        await send_message(context, reply[0])
        return
    for trivia_object in reply[0]:
        embed = trivia_object['embed']
        correct = trivia_object['correct']
        sent_message = await send_message(context, embed)

        # Add reactions to message
        for emoji in TRIVIA_EMOJIS:
            await sent_message.add_reaction(emoji)

        # Check if user answered correctly
        def check(user_reaction, reacting_user):
            # Check if the reaction is valid and from the same user and channel as the command
            return user_reaction.message.id == sent_message.id \
                and reacting_user.id == context.author.id \
                and str(user_reaction.emoji) in TRIVIA_EMOJIS

        try:
            # Wait for 10 seconds or until a valid reaction is added
            total_questions += 1
            reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await send_message(context, f'Sorry {context.author.name}, you ran out of time')
            break
        if correct == TRIVIA_EMOJIS.index(str(reaction.emoji)):
            successful_questions += 1
            await send_message(context, responses.trivia_response(True, user.name))
        else:
            await send_message(context, responses.trivia_response(False, user.name))
    # Update score
    await send_message(context, f'You scored {successful_questions}/{total_questions}')
    profiles.update_trivia_score(str(context.author), successful_questions, total_questions)


def run_discord_bot(token, prefix='.'):
    # Define bot intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running.')

    @bot.event
    async def on_message(context: discord.Message):
        if context.author == bot.user:
            return
        user_message = str(context.content).lower()
        if len(context.content) == 0:
            return
        if context.content[0] != prefix:
            return

        username = str(context.author)
        channel = str(context.channel)
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
        reply = await _process_command(command, argument, username, prefix)
        if command == 'dm':
            # Respond to the message
            if 'direct message' not in str(context.channel).lower():
                await send_message(context, reply[0])
            # Send a private message to the user.
            await send_message(context, reply[1], is_private=True)
        elif command in ['trivia', 'guess']:
            await _send_trivia_questions(bot, context, reply)
        else:
            try:
                await send_message(context, reply[0])
            except IndexError:
                pass

    bot.run(token)

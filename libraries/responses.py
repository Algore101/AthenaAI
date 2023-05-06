import random
import discord
from libraries import heroChooser, profiles, trivia
import os
import json
from discord import Embed

MISSPELLINGS_FILE = os.path.join(os.path.dirname(__file__), '../data/misspellings.json')


def _correct_spelling(hero_name: str) -> str:
    hero_name = hero_name.lower()

    with open(MISSPELLINGS_FILE, 'r', encoding='utf-8') as file:
        misspellings_data = dict(json.load(file))
        file.close()
        for hero, misspells in misspellings_data.items():
            if hero_name in misspells:
                hero_name = hero
                break

    return hero_name


def help_menu(**kwargs) -> str:
    response = 'Hi there! My name is *AthenaAI*, the Overwatch 2 hero choosing bot.\n' \
               'Below are all the ways you can interact with me!\n\n' \
               '**Get a hero:**\n' \
               '`{prefix}hero` `{prefix}all` – Returns a random hero from all the categories\n' \
               '`{prefix}tank` – Returns a random tank hero\n' \
               '`{prefix}damage` `{prefix}dps` – Returns a random damage hero\n' \
               '`{prefix}support` `{prefix}healer` – Returns a random support hero\n\n' \
               '**Get a duo:**\n' \
               'Add `duo` after any of the hero commands\n' \
               'E.g. `{prefix}support duo`\n\n' \
               '**Get a random duo:**\n' \
               'Add `rduo` after any of the hero commands\n' \
               'E.g. `{prefix}damage rduo`\n\n' \
               '**Select a role**\n' \
               '`{prefix}role` - Returns a random role to queue as\n\n' \
               '**Profile based commands:**\n' \
               '`{prefix}profile` - View your profile\n' \
               '`{prefix}avoid [hero]` - Adds the hero to your avoid list\n' \
               '`{prefix}unavoid [hero]` - Removes the hero from your avoid list\n' \
               '`{prefix}unavoid all` - Removes all heroes from your avoid list\n\n' \
               '**Other commands:**\n' \
               '`{prefix}dm` - Interact with me in your DMs\n' \
               '`{prefix}help` - Returns this message\n' \
               '`{prefix}list [role]` - Returns a list of all the heroes in the role\n'
    return response.format(prefix=kwargs['prefix'])


def choose_hero(**kwargs) -> str:
    username = kwargs['username']
    category = kwargs['category']
    prefix = kwargs['prefix']
    available_heroes = heroChooser.get_heroes_in_category(category)
    if len(available_heroes) == 0:
        return 'That is not a valid category. Please try using `{prefix}tank` `{prefix}damage` ' \
               '`{prefix}support` or `{prefix}all`'.format(prefix=prefix)
    # Remove avoided heroes
    available_heroes = [x for x in available_heroes if not profiles.is_hero_avoided(username, x)]

    if len(available_heroes) == 0:
        return 'I cannot suggest a hero to play because you have avoided everyone in this category.'

    hero = heroChooser.select_random_hero_in_category(category)
    while hero not in available_heroes:
        hero = heroChooser.select_random_hero_in_category(category)

    if hero == 'Winston':
        chance = random.randint(1, 10)
        if chance == 1:
            hero = 'Winton.'
    responses = [
        '{hero}',
        'Hmm... how about giving {hero} a shot?',
        'I suggest you play {hero}',
        'I do not know the context, but {hero} could work',
        'How about {hero}?',
        '{hero} might be a good pick'
    ]
    # Add hero specific responses
    additional_responses = []
    if hero == 'Lifeweaver':
        additional_responses = [
            'Since {hero} is new, why not try playing him?',
            'Have you played {hero} yet?',
            'If you have unlocked {hero}, try him out',
        ]
    responses += additional_responses
    return random.choice(responses).format(hero=hero)


def choose_duo(**kwargs) -> str:
    username = kwargs['username']
    category = kwargs['category']
    prefix = kwargs['prefix']
    random_duo = kwargs['random_duo']
    if category == 'tank':
        responses = [
            'This is Overwatch ***2***, meaning there is only one tank.',
            'Tank duos do not exist in Overwatch 2.',
            'Last I checked, there is only one tank.',
            '*[Sarcastically:]* Haha, very funny.',
            '...',
            'Overwatch 2 does not have two tanks.',
            'Overwatch 2 only has one tank.'
        ]
        return random.choice(responses)

    # Get available heroes
    available_heroes = heroChooser.get_heroes_in_category(category)
    if len(available_heroes) == 0:
        return 'That is not a valid category. Please try using `{prefix}tank` `{prefix}damage` ' \
               '`{prefix}support` or `{prefix}all`'.format(prefix=prefix)
    # Remove avoided heroes
    available_heroes = [x for x in available_heroes if not profiles.is_hero_avoided(username, x)]

    # Get number of matches
    all_duos = heroChooser.get_duos_in_category(category)
    matched_duos = []
    for duo in all_duos:
        if duo[0] in available_heroes or duo[1] in available_heroes:
            matched_duos.append(duo)

    if len(matched_duos) == 0:
        return 'There are no duos that I can suggest with your avoid list in mind.'

    if random_duo:
        duo = heroChooser.select_random_duo_in_category(category)
    else:
        duo = random.choice(matched_duos)

    return f'{duo[0]} & {duo[1]}'


def greet_privately(**kwargs) -> list:
    responses = [
        'Check your DMs ;)',
        'I sent you a little something <3',
    ]
    greetings = [
        'Hey there!',
        'Hello!',
        'Greetings!',
        'Hello world!',
        'Hi! I am AthenaAI, here to assist you in deciding on which Overwatch 2 hero to select.',
        'Hello there',
        'Welcome to my DMs.',
        'Now entering the chat.',
        'Traveling to the chatroom.',
        'Now arriving at your DMs.',
        'How can I help?',
        'How can I be of assistance?',
    ]
    return [random.choice(responses), random.choice(greetings)]


def get_profile(**kwargs) -> Embed:
    username = kwargs['username']
    # Update users
    profiles.update_trivia_score(username, 0, 0)
    user_data = profiles.get_profile(username)
    output = Embed(title=f'Profile: {username}', colour=discord.Color.from_rgb(38, 99, 199))
    # Get avoided heroes
    avoided_heroes = ''
    if len(user_data['avoided_heroes']) == 0:
        avoided_heroes = 'None\n'
    else:
        for hero in user_data['avoided_heroes']:
            avoided_heroes += f'{hero}\n'
    output.add_field(
        name='🚫 Avoided Heroes',
        value=avoided_heroes
    )
    # Get trivia score
    total_questions = int(user_data['total_questions'])
    if total_questions == 0:
        success_rate = 0
    else:
        success_rate = int(int(user_data['successful_questions']) / total_questions * 100)
    output.add_field(
        name='✏️ Trivia statistics',
        value=f'Success rate: {success_rate}%\n'
              f'Questions attempted: {total_questions}',
        inline=False
    )
    return output


def avoid_hero(**kwargs) -> str:
    username = kwargs['username']
    hero_to_avoid = kwargs['hero_to_avoid']
    prefix = kwargs['prefix']
    all_heroes = heroChooser.get_heroes_in_category('all')
    if len(hero_to_avoid) == 0:
        responses = [
            'I cannot read your mind, you know. You need to tell me which hero to avoid.',
            'Remember to include the name of the hero you want me to avoid.',
            'You forgot to tell me who to avoid.',
            'Alright, I will avoid suggesting- wait. You did not tell me which hero to avoid.',
            'In order for me to follow your command, I need all the information.',
        ]
        return f'{random.choice(responses)}\nE.g. `{prefix}avoid Symmetra`'

    # Correct common name spellings
    hero_to_avoid = _correct_spelling(hero_to_avoid)

    for hero in all_heroes:
        # Add hero to avoid list
        if hero_to_avoid.lower() == hero.lower():
            if not profiles.is_hero_avoided(username, hero):
                profiles.avoid_hero(username, hero)
                return f'Done! I will no longer suggest {hero}.'
            else:
                return f'I have already avoided {hero} for you.'
    return 'I could not seem to find the hero you entered. Please make sure you spelled their name correctly.'


def unavoid_hero(**kwargs) -> str:
    username = kwargs['username']
    hero_to_unavoid = kwargs['hero_to_unavoid']
    prefix = kwargs['prefix']
    all_heroes = heroChooser.get_heroes_in_category('all')
    if len(hero_to_unavoid) == 0:
        responses = [
            'I cannot read your mind, you know. You need to tell me which hero to unavoid.',
            'Remember to include the name of the hero you want me to unavoid.',
            'You forgot to tell me who to unavoid.',
            'In order for me to follow your command, I need all the information.',
        ]
        return f'{random.choice(responses)}\nE.g. `{prefix}unavoid Reinhardt`'

    # Correct common name spellings
    hero_to_unavoid = _correct_spelling(hero_to_unavoid)

    if hero_to_unavoid == 'all':
        for hero in all_heroes:
            profiles.unavoid_hero(username, hero)
        return 'I have cleared your avoid list for you.'
    else:
        for hero in all_heroes:
            # Remove hero from avoid list
            if hero_to_unavoid.lower() == hero.lower():
                if profiles.is_hero_avoided(username, hero):
                    profiles.unavoid_hero(username, hero)
                    return f'{hero} has been removed from your avoid list.'
                else:
                    return f'I cannot remove {hero} because you have not avoided them.'
    return 'If you want me to remove a hero from your avoid list, you are going to have to spell their name correctly.'


def choose_role(**kwargs):
    responses = [
        'You seem to be in a {role} mood.',
        'I suggest queuing for {role} heroes.',
        'How about {role}?',
        'Are you willing to give {role} a try?',
        'If I were you I would select {role}.',
        'You humans really are indecisive. Might I suggest {role}?',
        'You do know Overwatch 2 has a feature for this, right? It is called queueing as "All" and it is a lot '
        'simpler than typing that command.\nAnyway, I suggest playing {role}.',
    ]
    return random.choice(responses).format(role=heroChooser.select_role())


def duo(**kwargs):
    return 'Please try using `duo` as an argument and not a command.\n' \
           'E.g. `{prefix}support duo` for supports that work well together\n' \
           'Tip: Also try using `rduo` as an argument for two random heroes.'.format(prefix=kwargs['prefix'])


def rduo(**kwargs):
    return 'Please try using `rduo` as an argument and not a command.\n' \
           'E.g. `{prefix}damage rduo` for two random damage characters\n' \
           'Tip: Also try using `rduo` as an argument for two random heroes.'.format(prefix=kwargs['prefix'])


def get_heroes_in_category(**kwargs):
    category = kwargs['category']
    prefix = kwargs['prefix']
    if category == '':
        return 'Please try using "tank", "damage", "support" or "all" as an argument.\n' \
               'E.g. `{prefix}list all`'.format(prefix=prefix)
    heroes = heroChooser.get_heroes_in_category(category)
    if len(heroes) == 0:
        return 'That is not a valid role. Please try using "tank", "damage", "support" or "all" as an argument.\n' \
               'E.g. `{prefix}list all`'.format(prefix=prefix)
    if category == 'all':
        response = 'Here is a list of all the heroes:'
    else:
        response = f'Here are all the heroes in the {category.lower()} category:'

    for hero in heroes:
        response += f'\n- {hero}'

    return response


def get_trivia_question(**kwargs):
    prefix = kwargs['prefix']
    try:
        if kwargs['number_of_questions'] == '':
            return trivia.get_questions()
        else:
            number_of_questions = int(kwargs['number_of_questions'])
            return trivia.get_questions(number_of_questions)
    except ValueError:
        return 'Invalid argument for command `trivia`. Please enter a number for the amount of questions you want.' \
               'E.g. `{prefix}trivia 3`'.format(prefix=prefix)

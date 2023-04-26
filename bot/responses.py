import random
import heroChooser
import profiles


def _correct_spelling(hero_name: str) -> str:
    hero_name = hero_name.lower()
    # Tank heroes
    if hero_name in ['dva', 'd va']:
        hero_name = 'D.Va'
    elif hero_name in ['doom']:
        hero_name = 'Doomfist'
    elif hero_name in ['jq', 'queen']:
        hero_name = 'Junker Queen'
    elif hero_name in ['ram', 'ramatra']:
        hero_name = 'Ramattra'
    elif hero_name in ['rein', 'reinhart', 'reinhard']:
        hero_name = 'Reinhardt'
    elif hero_name in ['hog', 'road']:
        hero_name = 'Roadhog'
    elif hero_name in ['sig']:
        hero_name = 'Sigma'
    elif hero_name in ['monkey', 'winton', 'monki']:
        hero_name = 'Winston'
    elif hero_name in ['ball', 'hammond']:
        hero_name = 'Wrecking Ball'
    # Damage heroes
    elif hero_name in ['ash']:
        hero_name = 'Ashe'
    elif hero_name in ['cass']:
        hero_name = 'Cassidy'
    elif hero_name in ['junk', 'rat']:
        hero_name = 'Junkrat'
    elif hero_name in ['may']:
        hero_name = 'Mei'
    elif hero_name in ['farah', 'fara', 'phara']:
        hero_name = 'Pharah'
    elif hero_name in ['sojorn', 'sojurn', 'sojon', 'sojun']:
        hero_name = 'Sojourn'
    elif hero_name in ['soldier 76', 'soldier', '76']:
        hero_name = 'Soldier: 76'
    elif hero_name in ['sym', 'symm', 'symetra']:
        hero_name = 'Symmetra'
    elif hero_name in ['torbjorn', 'torb', 'torbyorn']:
        hero_name = 'Torbjörn'
    elif hero_name in ['widow']:
        hero_name = 'Widowmaker'
    # Support heroes
    elif hero_name in ['bap', 'baptist']:
        hero_name = 'Baptiste'
    elif hero_name in ['brig', 'brigit', 'brigite']:
        hero_name = 'Brigitte'
    elif hero_name in ['kiri']:
        hero_name = 'Kiriko'
    elif hero_name in ['life', 'weaver']:
        hero_name = 'Lifeweaver'
    elif hero_name in ['lucio']:
        hero_name = 'Lúcio'
    elif hero_name in ['zen', 'zenyata']:
        hero_name = 'Zenyatta'
    return hero_name


def help_menu() -> str:
    response = 'Hi there! My name is *AthenaAI*, the Overwatch 2 hero choosing bot.\n' \
               'Below are all the ways you can interact with me!\n\n' \
               '**Get a hero:**\n' \
               '`.hero` `.all` – Returns a random hero from all the categories\n' \
               '`.tank` – Returns a random tank hero\n' \
               '`.damage` `.dps` – Returns a random damage hero\n' \
               '`.support` `.healer` – Returns a random support hero\n\n' \
               '**Get a duo:**\n' \
               'Add `duo` after any of the hero commands\n' \
               'E.g. `.support duo`\n\n' \
               '**Get a random duo:**\n' \
               'Add `rduo` after any of the hero commands\n' \
               'E.g. `.damage rduo`\n\n' \
               '**Select a role**\n' \
               '`.role` - Returns a random role to queue as\n\n' \
               '**Profile based commands:**\n' \
               '`.profile` - View your profile\n' \
               '`.avoid [hero]` - Adds the hero to your avoid list\n' \
               '`.unavoid [hero]` - Removes the hero from your avoid list\n' \
               '`.unavoid all` - Removes all heroes from your avoid list\n\n' \
               '**Other commands:**\n' \
               '`.dm` - Interact with me in your DMs\n' \
               '`.help` - Returns this message\n'
    return response


def choose_hero(username, category) -> str:
    available_heroes = heroChooser.get_heroes_in_category(category)
    if len(available_heroes) == 0:
        return 'That is not a valid category. Please try using `.tank` `.damage` `.support` or `.all`'
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


def choose_duo(username, category, random_duo=True) -> str:
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
        return 'That is not a valid category. Please try using `.tank` `.damage` `.support` or `.all`'
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


def greet_privately() -> list:
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


def get_profile(username) -> str:
    user_data = profiles.get_profile(username)
    output = f'Profile: `{user_data["username"]}`\nAvoided heroes:\n'
    # Get avoided heroes
    if len(user_data['avoided_heroes']) > 0:
        for hero in user_data['avoided_heroes']:
            output += f'\t{hero}\n'
    else:
        output += '\tNone\n'
    # Get preferred heroes
    return output


def avoid_hero(username, hero_to_avoid: str) -> str:
    all_heroes = heroChooser.get_heroes_in_category('all')
    if len(hero_to_avoid) == 0:
        responses = [
            'I cannot read your mind, you know. You need to tell me which hero to avoid.',
            'Remember to include the name of the hero you want me to avoid.',
            'You forgot to tell me who to avoid.',
            'Alright, I will avoid suggesting- wait. You did not tell me which hero to avoid.',
            'In order for me to follow your command, I need all the information.',
        ]
        return f'{random.choice(responses)}\nE.g. `.avoid Symmetra`'

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


def unavoid_hero(username, hero_to_unavoid) -> str:
    all_heroes = heroChooser.get_heroes_in_category('all')
    if len(hero_to_unavoid) == 0:
        responses = [
            'I cannot read your mind, you know. You need to tell me which hero to unavoid.',
            'Remember to include the name of the hero you want me to unavoid.',
            'You forgot to tell me who to unavoid.',
            'In order for me to follow your command, I need all the information.',
        ]
        return f'{random.choice(responses)}\nE.g. `.unavoid Reinhardt`'

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


def choose_role():
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

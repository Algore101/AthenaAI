import random
import os
import discord
from discord.ext.commands import Bot
from discord import app_commands, Embed, Color
from libraries import profiles, heroChooser, classes
import json
from datetime import datetime

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
MISSPELLINGS_FILE = os.path.join(os.path.dirname(__file__), '../data/misspellings.json')
RANK_EMOJIS = ['🥇', '🥈', '🥉']
DEFAULT_EMBED_COLOUR = Color.from_rgb(38, 99, 199)


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


def _log_line(message: str):
    print(f'[{datetime.now()}]\t> {message}')


def run_discord_bot(token):
    # Define bot intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = Bot(command_prefix='[]', intents=intents)

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f'{bot.user} is now running!')

    # Get random hero/role
    @bot.tree.command(name='hero', description='Respond with a random hero in the selected role')
    @app_commands.describe(role='The role to get a hero from',
                           duo='The type of hero duo to return, `optimal` or `random`')
    @app_commands.choices(role=[
        app_commands.Choice(name='all', value='all'),
        app_commands.Choice(name='tank', value='tank'),
        app_commands.Choice(name='damage', value='damage'),
        app_commands.Choice(name='support', value='support')
    ], duo=[
        app_commands.Choice(name='optimal', value='optimal'),
        app_commands.Choice(name='random', value='random')
    ])
    async def get_hero(ctx, role: str = None, duo: str = None):
        """
        Respond with a random hero in the selected category

        :param ctx: The interaction that triggered this command
        :param role: The role to get a hero from
        :param duo: The type of hero duo to return, `optimal` or `random`
        :return:
        """
        _log_line(f'hero ({ctx.user})')
        if role is None:
            role = 'all'

        available_heroes = [x for x in heroChooser.get_heroes_in_category(role)
                            if not profiles.is_hero_avoided(str(ctx.user), x)]

        if len(available_heroes) == 0:
            await ctx.response.send_message(
                'I cannot suggest a hero to play because you have avoided everyone in this category.')
            return

        if duo is None:
            hero = heroChooser.select_random_hero_in_category(role)
            while hero not in available_heroes:
                hero = heroChooser.select_random_hero_in_category(role)

            if hero == 'Winston' and random.randint(1, 10) == 1:
                hero = 'Winton.'

            responses = [
                '{hero}',
                'Hmm... how about giving {hero} a shot?',
                'I suggest you play {hero}',
                'I do not know the context, but {hero} could work',
                'How about {hero}?',
                '{hero} might be a good pick'
            ]
            # Hero specific responses
            additional_responses = []
            if hero == 'Lifeweaver':
                additional_responses = [
                    'Since {hero} is new, why not try playing him?',
                    'Have you played {hero} yet?',
                    'If you have unlocked {hero}, try him out',
                ]
            responses += additional_responses
            await ctx.response.send_message(random.choice(responses).format(hero=hero))
        elif duo == 'random':
            if role == 'tank':
                responses = [
                    'This is Overwatch ***2***, meaning there is only one tank.',
                    'Tank duos do not exist in Overwatch 2.',
                    'Last I checked, there is only one tank.',
                    '*[Sarcastically:]* Haha, very funny.',
                    '...',
                    'Overwatch 2 does not have two tanks.',
                    'Overwatch 2 only has one tank.'
                ]
                await ctx.response.send_message(random.choice(responses))
                return
            response_duo = heroChooser.select_random_duo_in_category(role)
            while True:
                if response_duo[0] in available_heroes or response_duo[1] in available_heroes:
                    break
            await ctx.response.send_message(f'{response_duo[0]} & {response_duo[1]}')
        elif duo == 'optimal':
            if role == 'tank':
                responses = [
                    'This is Overwatch ***2***, meaning there is only one tank.',
                    'Tank duos do not exist in Overwatch 2.',
                    'Last I checked, there is only one tank.',
                    '*[Sarcastically:]* Haha, very funny.',
                    '...',
                    'Overwatch 2 does not have two tanks.',
                    'Overwatch 2 only has one tank.'
                ]
                await ctx.response.send_message(random.choice(responses))
                return
            all_duos = heroChooser.get_duos_in_category(role)
            matched_duos = []
            for hero_duo in all_duos:
                if hero_duo[0] in available_heroes or hero_duo[1] in available_heroes:
                    matched_duos.append(hero_duo)

            if len(matched_duos) == 0:
                await ctx.response.send_message('There are no duos that I can suggest with your avoid list in mind.')
                return

            response_duo = random.choice(matched_duos)
            await ctx.response.send_message(f'{response_duo[0]} & {response_duo[1]}')

    @bot.tree.command(name='role', description='Respond with a role')
    async def get_role(ctx):
        """
        Respond with a role

        :param ctx: The interaction that triggered this command
        :return:
        """
        _log_line(f'role ({ctx.user})')
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
        await ctx.response.send_message(random.choice(responses).format(role=heroChooser.select_role()))

    # Other commands
    # TODO: Rewrite help menu
    @bot.tree.command(name='help', description='Respond with a list of commands')
    async def get_help(ctx):
        """
        Respond with a list of commands

        :param ctx: The interaction that triggered this command
        :return:
        """
        _log_line(f'help ({ctx.user})')
        response = Embed(
            title='Help',
            description='Hi there! My name is *AthenaAI*, the Overwatch 2 hero choosing bot.\n'
                        '\n**NOTES:**\n'
                        'Arguments marked with an \\*asterisk are optional\n'
                        'The [docs](https://github.com/Algore101/AthenaAI/tree/master#readme) have more info\n'
                        '\n**COMMANDS:**\n',
            colour=DEFAULT_EMBED_COLOUR
        )
        response.add_field(name='/hero [\\*role] [\\*duo]', inline=False,
                           value='Respond with a random hero/duo in the selected role')
        response.add_field(name='/role', inline=False,
                           value='Respond with a role')
        response.add_field(name='/trivia [questions] [difficulty]', inline=False,
                           value='Play an Overwatch 2 hero trivia game')
        response.add_field(name='/guess [questions] [difficulty]', inline=False,
                           value='Play a game of "Guess The Hero"')
        response.add_field(name='/geoguess [questions] [difficulty]', inline=False,
                           value='Play a game of "Guess The Map"')
        response.add_field(name='/scoreboard', inline=False,
                           value='Show the top trivia players')
        response.add_field(name='/profile', inline=False,
                           value='View your profile')
        response.add_field(name='/avoid', inline=False,
                           value='Add a hero to your avoid list')
        response.add_field(name='/unavoid', inline=False,
                           value='Remove a hero from your avoid list')
        response.add_field(name='/help', inline=False,
                           value='Respond with a list of commands')
        response.add_field(name='/list [\\*role]', inline=False,
                           value='Respond with a list of all the heroes in the selected role')
        response.add_field(name='/dm', inline=False,
                           value='Interact with me in your DMs')
        await ctx.response.send_message(embed=response)

    @bot.tree.command(name='list', description='Respond with a list of all the heroes in the selected role')
    @app_commands.describe(role='The role to get the heroes from')
    @app_commands.choices(role=[
        app_commands.Choice(name='all', value='all'),
        app_commands.Choice(name='tank', value='tank'),
        app_commands.Choice(name='damage', value='damage'),
        app_commands.Choice(name='support', value='support')
    ])
    async def get_list(ctx, role: str = None):
        """
        Respond with a list of all the heroes in the selected role

        :param ctx: The interaction that triggered this command
        :param role: The role to get the heroes from
        :return:
        """
        _log_line(f'list ({ctx.user})')
        if role is None:
            role = 'all'

        heroes = heroChooser.get_heroes_in_category(role)
        response = f'{role.capitalize()} heroes:'
        for hero in heroes:
            response += f'\n- {hero}'
        await ctx.response.send_message(response)

    @bot.tree.command(name='dm', description='Interact with me in your DMs')
    async def dm(ctx):
        """
        Send the user a message in their DMs

        :param ctx: The interaction that triggered this command
        :return:
        """
        _log_line(f'dm ({ctx.user})')
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
        await ctx.response.send_message(random.choice(responses))
        await ctx.user.send(random.choice(greetings))

    # Profile based commands
    @bot.tree.command(name='profile', description='View your profile')
    async def get_profile(ctx):
        """
        Respond with information about the user

        :param ctx: The interaction that triggered this command
        :return:
        """
        _log_line(f'profile ({ctx.user})')
        # Update users
        profiles.update_trivia_score(str(ctx.user), 0, 0)
        user_data = profiles.get_profile(str(ctx.user))
        response = Embed(title=f'Profile: {str(ctx.user)}', colour=DEFAULT_EMBED_COLOUR)
        # Get avoided heroes
        avoided_heroes = ''
        if len(user_data['avoided_heroes']) == 0:
            avoided_heroes = 'None\n'
        else:
            for hero in user_data['avoided_heroes']:
                avoided_heroes += f'{hero}\n'
        response.add_field(
            name='🚫 Avoided Heroes',
            value=avoided_heroes
        )
        # Get trivia score
        if user_data['total_questions'] == 0:
            success_rate = 0
        else:
            success_rate = int(user_data['successful_questions'] / user_data['total_questions'] * 100)
        response.add_field(
            name='✏️ Trivia statistics',
            value=f'Success rate: {success_rate}%\n'
                  f'Questions attempted: {user_data["total_questions"]}',
            inline=False
        )
        await ctx.response.send_message(embed=response)

    @bot.tree.command(name='avoid', description='Add a hero to your avoid list')
    @app_commands.describe(hero='The name of the hero to avoid')
    async def avoid_hero(ctx, hero: str):
        """
        Add a hero to the user's avoid list

        :param ctx: The interaction that triggered this command
        :param hero: The name of the hero to avoid
        :return:
        """
        _log_line(f'avoid ({ctx.user})')
        hero = _correct_spelling(hero)
        for x in heroChooser.get_heroes_in_category('all'):
            if hero.lower() == x.lower():
                if not profiles.is_hero_avoided(str(ctx.user), x):
                    profiles.avoid_hero(str(ctx.user), x)
                    await ctx.response.send_message(f'Done! I will no longer suggest {x}.')
                else:
                    await ctx.response.send_message(f'I have already avoided {x} for you.')
                return

        await ctx.response.send_message('I could not seem to find the hero you entered. '
                                        'Please make sure you spelled their name correctly.')

    @bot.tree.command(name='unavoid', description='Remove a hero from your avoid list')
    @app_commands.describe(hero='The name of the hero to remove from your avoid list, all to clear avoid list')
    async def unavoid_hero(ctx, hero: str):
        """
        Remove a hero from the user's avoid list

        :param ctx: The interaction that triggered this command
        :param hero: The name of the hero to remove, `all` to clear avoid list
        :return:
        """
        _log_line(f'unavoid ({ctx.user})')
        if hero == 'all':
            for x in heroChooser.get_heroes_in_category('all'):
                profiles.unavoid_hero(str(ctx.user), x)
            await ctx.response.send_message('I have cleared your avoid list for you.')
            return
        else:
            hero = _correct_spelling(hero)
            for x in heroChooser.get_heroes_in_category('all'):
                if hero.lower() == x.lower():
                    if profiles.is_hero_avoided(str(ctx.user), x):
                        profiles.unavoid_hero(str(ctx.user), x)
                        await ctx.response.send_message(f'{x} has been removed from your avoid list.')
                    else:
                        await ctx.response.send_message(f'I cannot remove {x} because you have not avoided them.')
                    return
        await ctx.response.send_message('If you want me to remove a hero from your avoid list, '
                                        'you are going to have to spell their name correctly.')

    # Trivia commands

    # TODO Make an extreme difficulty
    # TODO Make an ability trivia

    # Lists of responses for the games
    positive = [
        "Well done!! :heart:",
        "Who has less of a life. The one who made the game or the one that plays it?",
        "You really know your stuff!",
        "Congrats! You have no life :black_heart:",
        "Touch some grass!",
        "Let's hope you can keep the streak going!",
        "Epic! You can remember useless stuff :heart:",
        "That was just a random guess that happened to be right.",
        "You are officially a nerd :nerd:",
        "Well, even a broken clock is right twice a day. Congratulations on getting that one correct.",
        "Oh, look at you, a veritable encyclopedia of Overwatch trivia. I suppose someone has to remember these things.",
        "You're not as clueless as I thought. I'm almost impressed. Almost.",
        "It seems you've stumbled upon the correct answer by accident. Beginner's luck, perhaps?",
        "Ah, a correct answer. Your brain must be a rare oasis in the desert of ignorance.",
        "Correct again. If only you could apply that knowledge to something more practical. Alas.",
        "Aha! You've managed to scrape together another correct response. It's almost as if you're trying."
    ]

    negative = [
        "Have you ever played a game of overwatch?",
        "Are you playing with the sound off?!",
        "This is actually embarrassing",
        "Come on...It really isn't that hard!",
        "Next one you'll get right!",
        "Someone needs to rewatch the animated shorts!",
        "Please go to: https://overwatch.fandom.com/wiki/Overwatch_Wiki",
        "Someone doesn't pay attention to the game :sob:",
        "Have you tried turning your monitor on?",
        "A baby knows more than you..",
        "Oh, bless your heart. That answer is so far off the mark, it's almost impressive.",
        "Not even close. I suppose there's a talent in consistently choosing the wrong path.",
        "Oh, dear. It seems your knowledge of Overwatch is as feeble as your attempt at this answer.",
        "Incorrect. Did you even bother to study? Or are you just here to waste everyone's time?",
        "Oh, the disappointment. Your answer is so wrong, it's as if you stumbled into the wrong game entirely.",
        "Nope, that's not even in the same galaxy as the correct answer. You're truly in a league of your own."
    ]
    more_wrong = [
        "Wrong again. Your lack of understanding is becoming a work of art in its own right.",
        "Another incorrect response. It's almost admirable how consistently you manage to fail.",
        "Incorrect, as expected. It must be a challenge to be so consistently clueless."
    ]

    @bot.tree.command(name='trivia', description='Play an Overwatch 2 hero trivia game')
    @app_commands.describe(difficulty='The difficulty level of the questions',
                           questions='The number of questions (limit of 10)')
    @app_commands.choices(difficulty=[
        app_commands.Choice(name='easy', value=1),
        app_commands.Choice(name='hard', value=2)
    ])
    async def play_trivia(interaction: discord.Interaction, questions: app_commands.Range[int, 1, 10],
                          difficulty: app_commands.Choice[int]):

        difficulty = difficulty.name
        rounds = questions
        player = interaction.user

        # Get the json file
        QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/questions.json')

        # Getting the information from the json file
        def _get_all_questions() -> dict:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as file:
                question_data = dict(json.load(file))
                file.close()
            return question_data

        # Store the information in a variable
        question_dict = _get_all_questions()

        # Make a copy to not remove anything from the original file
        facts = question_dict.get('facts').copy()

        # The score for the game
        score = 0

        await interaction.response.send_message(
            f'You want to play {rounds} rounds of trivia on {difficulty} difficulty :purple_heart:')

        # Start of the game
        for i in range(rounds):

            # Getting a random question from the json file
            random_question = random.choice(facts)

            # Getting the question itself
            question = random_question[difficulty]

            # Getting the correct answer
            correct_answer = random_question['correct']

            # Alternatives
            answer_list = question_dict.get('hero_list').copy()
            answer_list.remove(correct_answer)
            random.shuffle(answer_list)
            answers = [correct_answer, answer_list[1], answer_list[2], answer_list[3]]

            # Shuffle the answers
            random.shuffle(answers)

            # Getting the index of the correct answer
            correct_index = answers.index(correct_answer)

            # Getting the correct letter for the game
            correct_letter = ['A', 'B', 'C', 'D'][correct_index]

            # Answer text for the embed
            answer_text = '\n'.join([f"{letter}) {answer}" for letter, answer in zip(["A", "B", "C", "D"], answers)])

            # Remove the question to not get duplicates in the same game
            facts.remove(random_question)

            # Make the embed for the question
            embed = discord.Embed(title=f'Round {i + 1}', description=question)
            embed.add_field(name='Answers', value=answer_text)
            view = classes.TriviaView(question, correct_letter, player)
            await interaction.followup.send(embed=embed, view=view)
            await view.wait()

            # Check if the user answered correctly
            if view.response == correct_letter:
                await interaction.followup.send(random.choice(positive))
                score += 1
            else:
                if i + 1 - score < 2:
                    await interaction.followup.send(random.choice(negative))
                else:
                    await interaction.followup.send(random.choice(more_wrong))

        await interaction.followup.send(f'Game over! Your final score is {score}/{rounds} :heart:')

        """
        Respond with a number of trivia questions for the user to play

        :param ctx: The interaction that triggered this command
        :param questions: The number of questions
        :param difficulty: The difficulty level of the questions
        :return:
        """
        _log_line(f'trivia ({interaction.user})')

    @bot.tree.command(name='guess', description='Play a game of \"Guess The Hero\"')
    @app_commands.describe(difficulty='The difficulty level of the questions',
                           questions='The number of questions (limit of 10)')
    @app_commands.choices(difficulty=[
        app_commands.Choice(name='easy', value=1),
        app_commands.Choice(name='hard', value=2)
    ])
    async def play_guess(interaction: discord.Interaction, questions: app_commands.Range[int, 1, 10],
                         difficulty: app_commands.Choice[int]):

        """
                Respond with a number of guessing questions for the user to play

                :param interaction: The interaction that triggered this command
                :param questions: The number of questions
                :param difficulty: The difficulty level of the questions
                :return:
                """

        difficulty = difficulty.name
        rounds = questions
        player = interaction.user

        # Get the json file
        QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/questions.json')

        # Getting the information from the json file
        def _get_all_questions() -> dict:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as file:
                question_data = dict(json.load(file))
                file.close()
            return question_data

        # Store the information in a variable
        question_dict = _get_all_questions()

        # Make a copy to not remove anything from the original file
        images = question_dict.get('images').copy()

        # The score for the game
        score = 0

        await interaction.response.send_message(
            f'You want to play {rounds} rounds of Guess the Hero on {difficulty} difficulty :black_heart:')

        # Start of the game
        for i in range(rounds):

            # Getting a random question from the json file
            random_question = random.choice(images)

            # Getting the question itself
            question = random_question[difficulty]

            # Getting the correct answer
            correct_answer = random_question['correct']

            # Alternatives
            answer_list = question_dict.get('hero_list').copy()
            answer_list.remove(correct_answer)
            random.shuffle(answer_list)
            answers = [correct_answer, answer_list[1], answer_list[2], answer_list[3]]

            # Shuffle the answers
            random.shuffle(answers)

            # Getting the index of the correct answer
            correct_index = answers.index(correct_answer)

            # Getting the correct letter for the game
            correct_letter = ['A', 'B', 'C', 'D'][correct_index]

            # Answer text for the embed
            answer_text = '\n'.join([f"{letter}) {answer}" for letter, answer in zip(["A", "B", "C", "D"], answers)])

            # Remove the question to not get duplicates in the same game
            images.remove(random_question)

            # Make the embed for the question
            embed = discord.Embed(title=f'Round {i + 1}')
            embed.add_field(name='Answers', value=answer_text)
            embed.set_image(url=question)
            view = classes.TriviaView(question, correct_letter, player)
            await interaction.followup.send(embed=embed, view=view)
            await view.wait()

            # Check if the user answered correctly
            if view.response == correct_letter:
                await interaction.followup.send(random.choice(positive))
                score += 1
            else:
                if i + 1 - score < 2:
                    await interaction.followup.send(random.choice(negative))
                else:
                    await interaction.followup.send(random.choice(more_wrong))

        await interaction.followup.send(f'Game over! Your final score is {score}/{rounds} :heart:')

        _log_line(f'guess ({interaction.user})')

    @bot.tree.command(name='geoguess', description='Play a game of \"Guess The Map\"')
    @app_commands.describe(difficulty='The difficulty level of the questions',
                           questions='The number of questions (limit 10)')
    @app_commands.choices(difficulty=[
        app_commands.Choice(name='easy', value=1),
        app_commands.Choice(name='hard', value=2)
    ])
    async def play_geoguess(interaction: discord.Interaction, questions: app_commands.Range[int, 1, 10],
                            difficulty: app_commands.Choice[int]):
        """
        Respond with a number of map guessing questions for the user to play

        :param ctx: The interaction that triggered this command
        :param questions: The number of questions
        :param difficulty: The difficulty level of the questions
        :return:
        """

        difficulty = difficulty.name
        rounds = questions
        player = interaction.user

        # Get the json file
        QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/questions.json')

        # Getting the information from the json file
        def _get_all_questions() -> dict:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as file:
                question_data = dict(json.load(file))
                file.close()
            return question_data

        # Store the information in a variable
        question_dict = _get_all_questions()

        # Make a copy to not remove anything from the original file
        maps = question_dict.get('maps').copy()

        # The score for the game
        score = 0

        await interaction.response.send_message(
            f'You want to play {rounds} rounds of Guess the Hero on {difficulty} difficulty :black_heart:')

        # Start of the game
        for i in range(rounds):

            # Getting a random question from the json file
            random_question = random.choice(maps)

            # Getting the question itself
            question = random.choice(random_question[difficulty])

            # Getting the correct answer
            correct_answer = random_question['correct']

            # Alternatives
            answer_list = question_dict.get('maps_list').copy()
            answer_list.remove(correct_answer)
            random.shuffle(answer_list)
            answers = [correct_answer, answer_list[1], answer_list[2], answer_list[3]]

            # Shuffle the answers
            random.shuffle(answers)

            # Getting the index of the correct answer
            correct_index = answers.index(correct_answer)

            # Getting the correct letter for the game
            correct_letter = ['A', 'B', 'C', 'D'][correct_index]

            # Answer text for the embed
            answer_text = '\n'.join([f"{letter}) {answer}" for letter, answer in zip(["A", "B", "C", "D"], answers)])

            # Remove the question to not get duplicates in the same game
            maps.remove(random_question)

            # Make the embed for the question
            embed = discord.Embed(title=f'Round {i + 1}')
            embed.add_field(name='Answers', value=answer_text)
            embed.set_image(url=question)
            view = classes.TriviaView(question, correct_letter, player)
            await interaction.followup.send(embed=embed, view=view)
            await view.wait()

            # Check if the user answered correctly
            if view.response == correct_letter:
                await interaction.followup.send(random.choice(positive))
                score += 1
            else:
                if i + 1 - score < 2:
                    await interaction.followup.send(random.choice(negative))
                else:
                    await interaction.followup.send(random.choice(more_wrong))

        await interaction.followup.send(f'Game over! Your final score is {score}/{rounds} :heart:')

        _log_line(f'geoguess ({interaction.user})')

    @bot.tree.command(name='scoreboard', description='Show the top trivia players')
    async def get_scoreboard(ctx):
        """
        Respond with a scoreboard of all the trivia players

        :param ctx: The interaction that triggered this command
        :return:
        """
        _log_line(f'scoreboard ({ctx.user})')
        scoreboard = profiles.get_trivia_scoreboard()
        usernames = ''
        rate = ''
        total = ''
        # Get data
        for rank, user in enumerate(scoreboard):
            if rank < 3:
                usernames += RANK_EMOJIS[rank]
            usernames += f'{user["username"][:-5]}\n'
            success_rate = int(user['successful_questions'] / user['total_questions'] * 100)
            rate += f'{success_rate}%\n'
            total += f'{user["total_questions"]}\n'
        # Build embed
        response = Embed(title='Trivia scoreboard', description='Here are the top trivia players!',
                         colour=DEFAULT_EMBED_COLOUR)
        response.add_field(name='Username', value=usernames)
        response.add_field(name='Success Rate', value=rate)
        response.add_field(name='Questions attempted', value=total)
        await ctx.response.send_message(embed=response)

    bot.run(token)

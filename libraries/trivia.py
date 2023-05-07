import random
import json
import os
from discord import Embed, Color

TRIVIA_QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/questions.json')
EMOJIS = ["🇦", "🇧", "🇨", "🇩"]
LIMIT = 10
IMAGE_DIFFICULTIES = ['easy', 'hard']


def _get_data_from_file() -> dict:
    with open(TRIVIA_QUESTIONS_FILE, 'r', encoding='utf-8') as file:
        return dict(json.load(file))


def get_questions(number_of_questions: int = 1) -> list:
    """
    Creates questions as embeds and returns them as a dictionary

    :param number_of_questions: The number of questions to return with a limit of 10
    :return: A dictionary of embedded questions matched with their correct answers
    """
    # Open file
    questions_data = _get_data_from_file()['questions']
    # Store array of question embeds
    questions = []
    # Set limit
    if number_of_questions > LIMIT:
        number_of_questions = LIMIT

    for num in range(number_of_questions):
        # Get a random question
        data = random.choice(questions_data)
        question = data['question']
        answers = data['answers']
        correct = data['correct']
        questions_data.remove(data)

        # Create an embed message with the question and answers
        embed = Embed(
            title=f'Trivia Time! [{num + 1}/{number_of_questions}]',
            description=question,
            color=Color.random()
        )
        for i, answer in enumerate(answers):
            embed.add_field(name=EMOJIS[i], value=answer, inline=False)

        questions.append({'embed': embed, 'correct': correct})

    return questions


def get_images(number_of_images: int = 1, difficulty: str = 'easy') -> list:
    # Check for valid difficulty
    if difficulty.lower() not in IMAGE_DIFFICULTIES:
        difficulty = 'easy'
    # Open file
    images_data = _get_data_from_file()['images']
    # Store array of question embed
    images = []
    # Set limit
    if number_of_images > LIMIT:
        number_of_images = LIMIT

    for num in range(number_of_images):
        # Get random image
        data = random.choice(images_data)
        url = data[difficulty]
        answers = data['answers']
        correct = data['correct']
        images_data.remove(data)

        # Create an embed message with a question
        embed = Embed(
            title=f'Who is this? [{num + 1}/{number_of_images}]',
            colour=Color.random()
        )
        embed.set_image(url=url)

        for i, answer in enumerate(answers):
            embed.add_field(name=EMOJIS[i], value=answer, inline=False)

        images.append({'embed': embed, 'correct': correct})

    return images

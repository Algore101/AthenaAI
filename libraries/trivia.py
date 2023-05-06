import random
import json
import os
from discord import Embed, Color

TRIVIA_QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/questions.json')
EMOJIS = ["🇦", "🇧", "🇨", "🇩"]
LIMIT = 10


def get_questions(number_of_questions: int = 1) -> list:
    """
    Creates questions as embeds and returns them as a dictionary

    :param number_of_questions: The number of questions to return with a limit of 10
    :return: A dictionary of embedded questions matched with their correct answers
    """
    # Open file
    with open(TRIVIA_QUESTIONS_FILE, 'r', encoding='utf-8') as file:
        questions_data = list(json.load(file))
        file.close()

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

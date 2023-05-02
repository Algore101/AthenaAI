import random
import os
import json

HEROES_FILE = os.path.join(os.path.dirname(__file__), '../data/heroes.json')

heroes = dict(json.load(open(HEROES_FILE, 'r', encoding='utf-8')))['heroes']
duos = dict(json.load(open(HEROES_FILE, 'r', encoding='utf-8')))['duos']


def get_heroes_in_category(category=None) -> list:
    """
    Returns the names of all Overwatch heroes in the category.
    :param category: The hero category, e.g `tank`, `damage`, `support`, `all`.
    :return: An empty list if the category is not valid.
    """
    if category is None or category == 'all':
        all_heroes = []
        for hero_category in heroes:
            all_heroes += heroes[hero_category]
        return all_heroes

    try:
        return heroes[category]
    except KeyError:
        return []


def get_duos_in_category(category=None) -> list:
    """
    Returns a list of all valid hero duos in the category.
    :param category: The hero category, e.g `damage`, `support`, `all`.
    :return: An empty list if the category is not valid.
    """
    if category is None or category == 'all':
        all_duos = []
        for hero_category in duos:
            all_duos += duos[hero_category]
        return all_duos

    try:
        return duos[category]
    except KeyError:
        return []


def select_random_hero_in_category(category=None) -> str:
    """
    Select the name of a random Overwatch hero in the category.
    :param category: The hero category, e.g `tank`, `damage`, `support`, `all`.
    :return: The hero name as a string.
    """
    all_heroes = get_heroes_in_category(category)
    if len(all_heroes) > 0:
        return random.choice(all_heroes)
    return ''


def select_random_duo_in_category(category=None) -> list:
    """
    Selects two random Overwatch heroes in the category.
    :param category: The hero category, e.g `damage`, `support`, `all`.
    :return: [hero1, hero2] or an empty list for an invalid category.
    """
    if category == 'tank':
        return []
    hero1 = select_random_hero_in_category(category)
    hero2 = select_random_hero_in_category(category)
    if hero1 == '':
        return []
    while hero1 == hero2:
        hero2 = select_random_hero_in_category(category)
    return [hero1, hero2]


def select_duo_in_category(category=None) -> list:
    """
    Selects two Overwatch heroes in the category that play well together.
    :param category: The hero category, e.g `damage`, `support`, `all`.
    :return: [hero1, hero2] or an empty list for an invalid category.
    """
    if category == 'tank':
        return []

    duo_list = get_duos_in_category(category)

    if len(duo_list) == 0:
        return []

    return random.choice(duo_list)


def select_role() -> str:
    roles = list(heroes.keys())
    return random.choice(roles).capitalize()

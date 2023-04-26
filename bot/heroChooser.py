import random

heroes = {
    'tank': [
        "D.Va",
        "Doomfist",
        "Junker Queen",
        "Orisa",
        "Ramattra",
        "Reinhardt",
        "Roadhog",
        "Sigma",
        "Winston",
        "Wrecking Ball",
        "Zarya",
    ],
    'damage': [
        "Ashe",
        "Bastion",
        "Cassidy",
        "Echo",
        "Genji",
        "Hanzo",
        "Junkrat",
        "Mei",
        "Pharah",
        "Reaper",
        "Soldier: 76",
        "Sojourn",
        "Sombra",
        "Symmetra",
        "Torbjörn",
        "Tracer",
        "Widowmaker",
    ],
    'support': [
        "Ana",
        "Baptiste",
        "Brigitte",
        "Kiriko",
        "Lifeweaver",
        "Lucio",
        "Mercy",
        "Moira",
        "Zenyatta",
    ],
}
duos = {
    'damage': [
        ['Ashe', 'Echo'],
        ['Ashe', 'Hanzo'],
        ['Ashe', 'Junkrat'],
        ['Ashe', 'Pharah'],
        ['Bastion', 'Mei'],
        ['Cassidy', 'Mei'],
        ['Echo', 'Hanzo'],
        ['Echo', 'Sojourn'],
        ['Echo', 'Sombra'],
        ['Echo', 'Tracer'],
        ['Echo', 'Widowmaker'],
        ['Genji', 'Soldier: 76'],
        ['Genji', 'Tracer'],
        ['Hanzo', 'Junkrat'],
        ['Hanzo', 'Pharah'],
        ['Hanzo', 'Sojourn'],
        ['Hanzo', 'Sombra'],
        ['Hanzo', 'Tracer'],
        ['Hanzo', 'Widowmaker'],
        ['Junkrat', 'Sojourn'],
        ['Junkrat', 'Sombra'],
        ['Junkrat', 'Tracer'],
        ['Junkrat', 'Widowmaker'],
        ['Mei', 'Reaper'],
        ['Mei', 'Symmetra'],
        ['Pharah', 'Sojourn'],
        ['Pharah', 'Sombra'],
        ['Pharah', 'Tracer'],
        ['Pharah', 'Widowmaker'],
        ['Sombra', 'Tracer'],
    ],
    'support': [
        ['Ana', 'Lucio'],
        ['Ana', 'Mercy'],
        ['Ana', 'Zenyatta'],
        ['Baptiste', 'Brigitte'],
        ['Baptiste', 'Lucio'],
        ['Baptiste', 'Zenyatta'],
        ['Brigitte', 'Zenyatta'],
        ['Kiriko', 'Lucio'],
        ['Lucio', 'Moira'],
    ],
}


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

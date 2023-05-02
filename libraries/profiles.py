import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), '../data/users.json')


def make_account_if_none(username: str) -> None:
    # Check for account
    exists = False
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()

    for user in all_users:
        if user['username'] == username:
            exists = True
            break

    # Make account
    if not exists:
        new_user = {
            'username': username,
            'avoided_heroes': [],
            'preferred_heroes': []
        }
        all_users.append(new_user)
        with open(USERS_FILE, 'w', encoding='utf-8') as file:
            json.dump(all_users, file, indent=4, separators=(',', ': '), ensure_ascii=False)
            file.close()


def get_profile(username: str) -> dict:
    make_account_if_none(username)
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()

    for user in all_users:
        if user['username'] == username:
            return user


def is_hero_avoided(username: str, hero: str) -> bool:
    make_account_if_none(username)
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()

    user = {}
    for x in all_users:
        if x['username'] == username:
            user = x
            break
    avoided_heroes = user['avoided_heroes']
    if hero in avoided_heroes:
        return True
    return False


def avoid_hero(username: str, hero: str) -> None:
    make_account_if_none(username)
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()

    user = {}
    for x in all_users:
        if x['username'] == username:
            user = x
            break

    avoided_heroes = user['avoided_heroes']
    avoided_heroes.append(hero)
    user.update({'avoided_heroes': avoided_heroes})
    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)] = user
            break
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(all_users, file, indent=4, separators=(',', ': '), ensure_ascii=False)
        file.close()


def unavoid_hero(username: str, hero: str) -> None:
    make_account_if_none(username)
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()

    user = {}
    for x in all_users:
        if x['username'] == username:
            user = x
            break
    avoided_heroes = user['avoided_heroes']
    if hero in avoided_heroes:
        avoided_heroes.remove(hero)
    user.update({'avoided_heroes': avoided_heroes})
    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)] = user
            break
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(all_users, file, indent=4, separators=(',', ': '), ensure_ascii=False)
        file.close()

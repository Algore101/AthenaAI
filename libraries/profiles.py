import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), '../data/users.json')


def _get_all_users() -> list:
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        all_users = json.load(file)
        file.close()
    return all_users


def _update_user_file(new_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, separators=(',', ': '), ensure_ascii=False)
        file.close()


def _make_account_if_none(username: str) -> None:
    # Check for account
    exists = False
    all_users = _get_all_users()

    for user in all_users:
        if user['username'] == username:
            exists = True
            break

    # Make account
    if not exists:
        new_user = {
            'username': username,
            'avoided_heroes': [],
            'successful_questions': 0,
            'total_questions': 0,
            'opted_out': False,
        }
        all_users.append(new_user)
        _update_user_file(all_users)


def get_profile(username: str) -> dict:
    _make_account_if_none(username)
    for user in _get_all_users():
        if user['username'] == username:
            return user


def is_hero_avoided(username: str, hero: str) -> bool:
    _make_account_if_none(username)
    user = {}
    for x in _get_all_users():
        if x['username'] == username:
            user = x
            break
    avoided_heroes = user['avoided_heroes']
    if hero in avoided_heroes:
        return True
    return False


def avoid_hero(username: str, hero: str) -> None:
    _make_account_if_none(username)
    all_users = _get_all_users()

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
    _update_user_file(all_users)


def unavoid_hero(username: str, hero: str) -> None:
    _make_account_if_none(username)
    all_users = _get_all_users()

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
    _update_user_file(all_users)


def update_trivia_score(username: str, successful_questions: int, total_questions: int):
    _make_account_if_none(username)
    all_users = _get_all_users()

    user = {}
    for x in all_users:
        if x['username'] == username:
            user = x
            break
    try:
        s_questions = user['successful_questions']
        s_questions += successful_questions
        t_questions = user['total_questions']
        t_questions += total_questions
    except KeyError:
        s_questions = 0
        t_questions = 0
    user.update({'successful_questions': s_questions, 'total_questions': t_questions})
    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)] = user
            break
    _update_user_file(all_users)


def get_trivia_scoreboard() -> list:
    def get_success_rate(user: dict):
        return int(user['successful_questions'] / user['total_questions'] * 100)

    return sorted(_get_all_users(), key=lambda i: (get_success_rate(i), i['total_questions']), reverse=True)


def reset_trivia_score(username: str):
    all_users = _get_all_users()

    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)]['successful_questions'] = 0
            all_users[all_users.index(x)]['total_questions'] = 0

    _update_user_file(all_users)


def opt_out(username: str):
    _make_account_if_none(username)
    all_users = _get_all_users()

    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)] = {'username': username, 'opted_out': True}

    _update_user_file(all_users)


def opt_in(username: str):
    all_users = _get_all_users()

    for x in all_users:
        if x['username'] == username and x['opted_out'] is True:
            all_users.pop(all_users.index(x))

    _update_user_file(all_users)
    _make_account_if_none(username)


def is_opted_out(username: str) -> bool:
    all_users = _get_all_users()

    for x in all_users:
        if x['username'] == username and x['opted_out'] is True:
            return True
    return False

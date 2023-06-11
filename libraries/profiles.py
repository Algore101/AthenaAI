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
            'trivia_success': 0,
            'trivia_total': 0,
            'guess the hero_success': 0,
            'guess the hero_total': 0,
            'mapguessr_success': 0,
            'mapguessr_total': 0
        }
        all_users.append(new_user)
        _update_user_file(all_users)


def get_profile(username: str):
    _make_account_if_none(username)
    for user in _get_all_users():
        if user['username'] == username:
            return user
    return None


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


def update_game_score(username: str, game: str, successful_questions: int, total_questions: int):
    _make_account_if_none(username)
    all_users = _get_all_users()

    user = {}
    if game not in ['trivia', 'guess the hero', 'mapguessr']:
        return
    for x in all_users:
        if x['username'] == username:
            user = x
            break
    try:
        s_questions = user[f'{game}_success']
        s_questions += successful_questions
        t_questions = user[f'{game}_total']
        t_questions += total_questions
    except KeyError:
        s_questions = 0
        t_questions = 0
    user.update({f'{game}_success': s_questions, f'{game}_total': t_questions})
    for x in all_users:
        if x['username'] == username:
            all_users[all_users.index(x)] = user
            break
    _update_user_file(all_users)


def get_game_scoreboard(game: str = None) -> list or None:
    if game not in ['trivia', 'guess the hero', 'mapguessr'] and game is not None:
        return []
    elif game is None:
        scoreboard = []
        for user in _get_all_users():
            user_score = 0
            user_total = 0
            for g in ['trivia', 'guess the hero', 'mapguessr']:
                user_score += user[f'{g}_success']
                user_total += user[f'{g}_total']
            scoreboard.append({'username': user['username'],
                               'success': user_score,
                               'total': user_total})
        return sorted(scoreboard, key=lambda i: int(i['success'] / i['total'] * 100), reverse=True)

    scoreboard = []
    for user in _get_all_users():
        if user[f'{game}_total'] > 0:
            scoreboard.append(user)

    def get_success_rate(user: dict):
        return int(user[f'{game}_success'] / user[f'{game}_total'] * 100)

    return sorted(scoreboard, key=lambda i: (get_success_rate(i), i[f'{game}_total']), reverse=True)


def delete(username: str):
    all_users = _get_all_users()

    for x in all_users:
        if x['username'] == username:
            all_users.remove(x)

    _update_user_file(all_users)

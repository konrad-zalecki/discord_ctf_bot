import sqlite3
import functools
from datetime import datetime
from database_logic import get_event_name, get_event_levels


def get_leaderboard_data(event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT user_id, current_level, last_solution FROM user_subscriptions WHERE event_id={event_id}')
    leaderboard = c.fetchall()
    conn.close()
    return leaderboard


def sort_leaderboard_data(data):
    def leaderboard_data_comparator(lhs, rhs):
        if lhs[1] > rhs[1]:
            return -1
        elif lhs[1] == rhs[1]:
            if lhs[1] == 1:
                return 0
            else:
                lhs_datetime = datetime.strptime(lhs[2], '%Y-%m-%d %H:%M:%S')
                rhs_datetime = datetime.strptime(rhs[2], '%Y-%m-%d %H:%M:%S')
                if lhs_datetime < rhs_datetime:
                    return -1
                elif lhs_datetime > rhs_datetime:
                    return 1
                return 0
        else:
            return 1
    return sorted(data, key=functools.cmp_to_key(leaderboard_data_comparator))


def create_leaderboard_message(data, event_levels, event_name):
    if len(data) == 0:
        return 'Noone is registered for this event yet.'
    message = f'=== Event leaderboard for "{event_name}" ===\n'
    current_index = 0
    current_place = 1
    while current_index < len(data) and data[current_index][1] > 1:
        user_id, level, last_solution = data[current_index]
        new_line = '{0: >3}'.format(str(current_place) + '.') + f' <@{user_id}> ({level - 1}/{event_levels})'
        if level > 1:
            new_line += f', level {level - 1} solved at {last_solution}.'
        message += new_line + '\n'
        current_index += 1
        current_place += 1
    if current_index == 0:
        message += "Looks like first blood hasn't been scored yet!\n"
    if current_index < len(data):
        message += '\nRegistered users with no solutions:\n'
        while current_index < len(data):
            message += f'<@{data[current_index][0]}>\n'
            current_index += 1
    return message


def get_leaderboard(event_id):
    event_name = get_event_name(event_id)
    event_levels = get_event_levels(event_id)
    leaderboard_data = get_leaderboard_data(event_id)
    leaderboard_data = sort_leaderboard_data(leaderboard_data)
    return create_leaderboard_message(leaderboard_data, event_levels, event_name)


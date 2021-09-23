import sqlite3

def get_event_id(event_name):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT event_id FROM events WHERE event_name="{event_name.lower()}"')
    found_ids = c.fetchall()
    conn.close()
    if len(found_ids) == 0:
        return None
    else:
        return found_ids[0][0]


# assumes event_id is existing value
def get_event_name(event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT event_name FROM events WHERE event_id={event_id}')
    query_records = c.fetchall()
    conn.close()
    return query_records[0][0]


# assumed event_id is existing value
def get_problem_name(event_id, level):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT problem_name FROM problems WHERE event_id={event_id} AND event_level={level}')
    query_records = c.fetchall()
    conn.close()
    return query_records[0][0]


def is_channel_registered(channel_object, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM channel_subscriptions WHERE channel_id="{channel_object.id}" AND event_id={event_id}')
    records_found = len(c.fetchall())
    conn.close()
    return records_found > 0


def register_channel(channel_object, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    if is_channel_registered(channel_object, event_id):
        conn.close()
        return False
    c.execute(f'INSERT INTO channel_subscriptions(channel_id, event_id) VALUES ({channel_object.id}, {event_id})')
    conn.commit()
    conn.close()
    return True


def is_user_registered(user_object, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_subscriptions WHERE user_id="{user_object.id}"')
    records_found = len(c.fetchall())
    conn.close()
    return records_found == 1


def register_user(user_object, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    if is_user_registered(user_object, event_id):
        conn.close()
        return False
    c.execute(f'INSERT INTO user_subscriptions(user_id, event_id) VALUES ({user_object.id}, {event_id})')
    conn.commit()
    conn.close()
    return True


# assumes event_id is existing value
def get_event_levels(event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT levels FROM events WHERE event_id={event_id}')
    query_records = c.fetchall()
    conn.close()
    return query_records[0][0]


def get_all_events():
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT event_id FROM events')
    query_records = c.fetchall()
    conn.close()
    return [item[0] for item in query_records]


def get_registered_events(channel_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT event_id FROM channel_subscriptions WHERE channel_id={channel_id}')
    query_records = c.fetchall()
    conn.close()
    return [item[0] for item in query_records]


# assumes that user with given id is registered to event with given id
def get_user_current_level_in_event(user_id, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT current_level FROM user_subscriptions WHERE user_id={user_id} AND event_id={event_id}')
    user_level = c.fetchall()[0][0]
    conn.close()
    return user_level


def did_finish_event(user_id, event_id):
    return get_user_current_level_in_event(user_id, event_id) > get_event_levels(event_id)


def get_level_flag(event_id, level_number):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT problem_flag FROM problems WHERE event_id={event_id} AND event_level={level_number}')
    level_flag =  c.fetchall()[0][0]
    conn.close()
    return level_flag


# assumes user is registered to the event and did not finish it yet
def is_correct_solution(user_id, event_id, flag):
    user_level = get_user_current_level_in_event(user_id, event_id)
    correct_flag = get_level_flag(event_id, user_level)
    return correct_flag.lower() == flag.lower()


def level_up(user_id, event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'UPDATE user_subscriptions SET current_level=current_level+1, last_solution=DATETIME(\'now\') WHERE user_id={user_id} AND event_id={event_id}')
    conn.commit()
    conn.close()


# assumes given event_id is valid
def get_subscribing_channels(event_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT channel_id FROM channel_subscriptions WHERE event_id={event_id}')
    query_records = c.fetchall()
    conn.close()
    return [item[0] for item in query_records]


def get_all_events_subscribed_for_user(user_id):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT event_id FROM user_subscriptions WHERE user_id={user_id}')
    query_records = c.fetchall()
    conn.close()
    return [item[0] for item in query_records]


def how_many_completions(event_id):
    event_levels = get_event_levels(event_id)
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_subscriptions WHERE current_level>{event_levels}')
    completions =  len(c.fetchall())
    conn.close()
    return completions
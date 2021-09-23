import sqlite3

def main():

    conn = sqlite3.connect('ctf-bot.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE events (
        event_id integer NOT NULL PRIMARY KEY,
        event_name text NOT NULL UNIQUE,
        levels integer NOT NULL
        )""")

    c.execute("""CREATE TABLE problems (
        problem_id integer NOT NULL PRIMARY KEY,
        event_level integer NOT NULL,
        event_id integer NOT NULL,
        problem_name text NOT NULL,
        problem_flag text NOT NULL
        )""")

    c.execute("""CREATE TABLE channel_subscriptions (
        channel_id integer NOT NULL,
        event_id integer NOT NULL,
        PRIMARY KEY(channel_id, event_id)
        )""")

    c.execute("""CREATE TABLE user_subscriptions (
        user_id integer NOT NULL,
        event_id integer NOT NULL,
        current_level integer DEFAULT 1,
        last_solution datetime,
        PRIMARY KEY(user_id, event_id)
        )""")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
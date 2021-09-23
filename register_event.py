import sqlite3
import os
import pathlib

def create_event(event_name, number_of_levels):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'INSERT INTO events(event_name, levels) VALUES ("{event_name}", {number_of_levels})')
    c.execute(f'SELECT event_id FROM events WHERE event_name="{event_name}"')
    event_id = c.fetchall()[0][0]
    conn.commit()
    conn.close()
    return event_id


def create_problem(event_id, level, name, flag):
    conn = sqlite3.connect('ctf-bot.db')
    c = conn.cursor()
    c.execute(f'INSERT INTO problems(event_id, event_level, problem_name, problem_flag) VALUES ({event_id}, {level}, "{name}", "{flag}")')
    conn.commit()
    conn.close()


def main():
    event_name = input('Name of event you want to register: ')
    event_dir = str(pathlib.Path(__file__).parent.resolve()) + '\\events\\' + event_name
    levels_dirs = os.listdir(event_dir)
    event_id = create_event(event_name, len(levels_dirs))
    for dir_name in levels_dirs:
        dir_path = event_dir + '\\' + dir_name
        flag_file = open(dir_path + '\\' + 'flag.txt')
        flag_content = flag_file.read().replace('\n', '')
        flag_file.close()
        name_file = open(dir_path + '\\' + 'name.txt')
        name_content = name_file.read().replace('\n', '')
        name_file.close()
        create_problem(event_id, int(dir_name), name_content, flag_content)
        

if __name__ == '__main__':
    main()
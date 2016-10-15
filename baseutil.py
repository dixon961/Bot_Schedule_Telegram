import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()


def add_user(user_id, group):
    enter_db()
    if len(c.execute('SELECT * FROM users WHERE user_id={id}'.format(id=user_id)).fetchall()) == 0:
        c.execute('INSERT INTO users VALUES ({id}, \'{group}\');'.format(id=user_id, group=str(group)))
        conn.commit()
    close_db()


def change_group(user_id, group):
    enter_db()
    c.execute('UPDATE users SET group_name=\'{group}\'WHERE user_id={id};'.format(group=group, id=user_id))
    conn.commit()
    close_db()


def get_group_by_user(user_id):
    enter_db()
    if c.execute('SELECT group_name FROM users WHERE user_id={id}'.format(id=user_id)).fetchall():
        ret = str(c.execute('SELECT group_name FROM users WHERE user_id={id}'.format(id=user_id)).fetchall()[0][0])
    else:
        ret = 'МП-42'

    close_db()
    return ret


def select_all():
    enter_db()
    ret = c.execute('SELECT * FROM users').fetchall()
    close_db()
    return ret


def enter_db():
    global conn
    conn = sqlite3.connect('users.db', check_same_thread=False)
    global c
    c = conn.cursor()


def close_db():
    c.close()
    conn.close()

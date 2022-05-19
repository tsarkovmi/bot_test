# DATABASE FUNCTIONS FOR DEADLINE_BOT

import sqlite3
import datetime


# insert user in database
def insert_user(user_id: int, tg_name: str, name: str, email: str, notifications_state: str, group_n: str):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # insert user into users table
    cursor.execute("""INSERT INTO users 
                    (user_id, tg_name, name, email, notifications_state) 
                    VALUES (:user_id, :tg_name, :name, :email, :notifications_state)""",
                   {'user_id': user_id, 'tg_name': tg_name, 'name': name,
                    'email': email, 'notifications_state': notifications_state})

    # get group_id
    cursor.execute("SELECT id FROM groups WHERE group_n=:group_n", {'group_n': group_n})
    group_id = cursor.fetchone()
    if not group_id:  # if there is no such group
        cursor.execute("INSERT INTO groups (group_n) VALUES (:group_n)", {'group_n': group_n})
        cursor.execute("SELECT id FROM groups WHERE group_n=:group_n", {'group_n': group_n})
        group_id = cursor.fetchone()

    # add group_id to the user record
    cursor.execute("UPDATE users SET group_id=:group_id WHERE user_id=:user_id",
                   {'group_id': group_id[0], 'user_id': user_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# insert deadline in db
def insert_deadline(user_id: int, deadline_name: str, day: int, month: int, year: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # insert deadline into deadlines table
    cursor.execute("INSERT INTO deadlines (deadline_name, day, month, year) "
                   "VALUES (:deadline_name, :day, :month, :year)",
                   {'deadline_name': deadline_name, 'day': day, 'month': month, 'year': year})

    # add group_id to deadline record
    cursor.execute("SELECT max(id) FROM deadlines")
    deadline_id = cursor.fetchone()[0]
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id", {'user_id': user_id})
    group_id = cursor.fetchone()[0]
    cursor.execute("UPDATE deadlines SET group_id=:group_id WHERE id=:deadline_id",
                   {'group_id': group_id, 'deadline_id': deadline_id})

    # get current date
    current_date = datetime.datetime.now()

    # add record to the logs table
    cursor.execute("INSERT INTO logs (deadline_name, group_id, action, user_id, day, month, year) "
                   "VALUES (:deadline_name, :group_id, 'создан', :user_id, :day, :month, :year)",
                   {'deadline_name': deadline_name, 'group_id': group_id, 'user_id': user_id, 'day': current_date.day,
                    'month': current_date.month, 'year': current_date.year})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# delete deadline from db
# returns 0 if everything OK, 1 - this deadline not from this user's group,
# 2 - there is no deadline with this deadline_id
def delete_deadline(user_id: int, deadline_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # !!!!!!MAY BE UNNECESSARY!!!!!!!!!!!!!!!!!!!!!!
    # check if deadline doesn't belong to this user's group
    cursor.execute("SELECT group_id FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_group_id = cursor.fetchone()[0]
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id", {'user_id': user_id})
    user_group_id = cursor.fetchone()[0]
    if user_group_id != deadline_group_id:
        return 1
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get deadline name
    cursor.execute("SELECT deadline_name FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_name = cursor.fetchone()
    # !!!!!!MAY BE UNNECESSARY!!!!!!!!!!!!!!!!!!!!!!
    if not deadline_name:  # if list there is no deadline with this deadline_id
        return 2
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get current date
    current_date = datetime.datetime.now()

    # add record to the logs table
    cursor.execute("INSERT INTO logs (deadline_name, group_id, action, user_id, day, month, year) "
                   "VALUES (:deadline_name, :group_id, 'удалён', :user_id, :day, :month, :year)",
                   {'deadline_name': deadline_name[0], 'group_id': deadline_group_id, 'user_id': user_id,
                    'day': current_date.day, 'month': current_date.month, 'year': current_date.year})

    # remove deadline
    cursor.execute("DELETE FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# returns list of deadlines for this user (for his group)
def get_deadlines(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get group_id
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id;", {'user_id': user_id})
    group_id = cursor.fetchone()[0]

    # get list of deadlines belongs to this group
    cursor.execute("SELECT * FROM deadlines WHERE group_id=:group_id ORDER BY year, month, day;",
                   {'group_id': group_id})
    deadlines = cursor.fetchall()

    # disconnect db and return list
    conn.close()
    return deadlines


# returns list of hot deadlines (less than 7 days) for this user (for his group)
def get_hot_deadlines(user_id: int):
    # get deadlines list and create empty hot_deadlines list
    deadlines = get_deadlines(user_id)
    hot_deadlines = []
    hot_deadlines_counter = 0

    # get current date
    current_date = datetime.datetime.now()

    # putting only hot deadlines in hot_deadlines list
    for i in range(len(deadlines)):
        # get deadline date
        deadline_day = deadlines[i][3]
        deadline_month = deadlines[i][4]
        deadline_year = deadlines[i][5]
        deadline_date = datetime.datetime(deadline_year, deadline_month, deadline_day)
        difference = (deadline_date - current_date).days
        if 7 >= difference >= -1:
            hot_deadlines.insert(hot_deadlines_counter, deadlines[i])
            hot_deadlines_counter = hot_deadlines_counter + 1

    # return list of hot deadlines
    return hot_deadlines


# update full name in user record
def update_name(user_id: int, new_name: str):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # update name
    cursor.execute("UPDATE users SET name=:new_name WHERE user_id=:user_id;",
                   {'new_name': new_name, 'user_id': user_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# update group in user record
def update_group(user_id: int, new_group_n: str):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # find out if group already in db and get new_group_id
    cursor.execute("SELECT id FROM groups WHERE group_n=:new_group_n;", {'new_group_n': new_group_n})
    new_group_id = cursor.fetchone()
    if not new_group_id:  # if there is no group with such group_n
        cursor.execute("INSERT INTO groups (group_n) VALUES (:new_group_n);", {'new_group_n': new_group_n})
        cursor.execute("SELECT id FROM groups WHERE group_n=:new_group_n;", {'new_group_n': new_group_n})
        new_group_id = cursor.fetchone()

    # update group_id in user record
    cursor.execute("UPDATE users SET group_id=:new_group_id "
                   "WHERE user_id=:user_id;",
                   {'new_group_id': new_group_id[0], 'user_id': user_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# change notifications_state in user record
def change_notifications_state(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get current_notifications_state
    cursor.execute("SELECT notifications_state FROM users WHERE user_id=:user_id;", {'user_id': user_id})
    current_notifications_state = cursor.fetchone()

    # update user record
    if current_notifications_state[0] == 'on':
        cursor.execute("UPDATE users SET notifications_state='off' WHERE user_id=:user_id;",
                       {'user_id': user_id})
    else:
        cursor.execute("UPDATE users SET notifications_state='on' WHERE user_id=:user_id;",
                       {'user_id': user_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# returns user info
def get_user_info(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get user info
    cursor.execute("SELECT * FROM users WHERE user_id=:user_id;", {'user_id': user_id})
    user_info = cursor.fetchone()

    # disconnect db and return user info
    conn.close()
    return user_info


# returns logs for user's group
def get_logs(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get group_id
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id;", {'user_id': user_id})
    group_id = cursor.fetchone()[0]

    # get logs for this group
    cursor.execute("SELECT * FROM logs WHERE group_id=:group_id;", {'group_id': group_id})
    logs = cursor.fetchall()

    # disconnect db and return user info
    conn.close()
    return logs


def get_all_users_ids():
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get user info
    cursor.execute("SELECT user_id FROM users")
    users_ids = cursor.fetchall()

    # disconnect db and return user info
    conn.close()
    return users_ids


def get_all_tg_names():
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # get user info
    cursor.execute("SELECT tg_name FROM users")
    tg_names = cursor.fetchall()

    # disconnect db and return user info
    conn.close()
    return tg_names


def update_deadline_name(deadline_id: int, new_name: str, user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_group_id = cursor.fetchone()[0]
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id", {'user_id': user_id})
    user_group_id = cursor.fetchone()[0]
    if user_group_id != deadline_group_id:
        return 1
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get deadline name
    cursor.execute("SELECT deadline_name FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_name = cursor.fetchone()
    # !!!!!!MAY BE UNNECESSARY!!!!!!!!!!!!!!!!!!!!!!
    if not deadline_name:  # if list there is no deadline with this deadline_id
        return 2
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get current date
    current_date = datetime.datetime.now()

    # add record to the logs table
    cursor.execute("INSERT INTO logs (deadline_name, group_id, action, user_id, day, month, year) "
                   "VALUES (:deadline_name, :group_id, 'изменено имя', :user_id, :day, :month, :year)",
                   {'deadline_name': deadline_name[0], 'group_id': deadline_group_id, 'user_id': user_id,
                    'day': current_date.day, 'month': current_date.month, 'year': current_date.year})

    cursor.execute("UPDATE deadlines SET deadline_name=:new_name "
                   "WHERE id=:deadline_id;",
                   {'new_name': new_name, 'deadline_id': deadline_id})
    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


def update_deadline_date(deadline_id: int, new_day: int, new_month: int, new_year: int,user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_group_id = cursor.fetchone()[0]
    cursor.execute("SELECT group_id FROM users WHERE user_id=:user_id", {'user_id': user_id})
    user_group_id = cursor.fetchone()[0]
    if user_group_id != deadline_group_id:
        return 1
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get deadline name
    cursor.execute("SELECT deadline_name FROM deadlines WHERE id=:deadline_id", {'deadline_id': deadline_id})
    deadline_name = cursor.fetchone()
    # !!!!!!MAY BE UNNECESSARY!!!!!!!!!!!!!!!!!!!!!!
    if not deadline_name:  # if list there is no deadline with this deadline_id
        return 2
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # get current date
    current_date = datetime.datetime.now()

    # add record to the logs table
    cursor.execute("INSERT INTO logs (deadline_name, group_id, action, user_id, day, month, year) "
                   "VALUES (:deadline_name, :group_id, 'изменена дата', :user_id, :day, :month, :year)",
                   {'deadline_name': deadline_name[0], 'group_id': deadline_group_id, 'user_id': user_id,
                    'day': current_date.day, 'month': current_date.month, 'year': current_date.year})

    cursor.execute("UPDATE deadlines SET day=:new_day, month=:new_month, year=:new_year "
                   "WHERE id=:deadline_id;",
                   {'new_day': new_day, 'new_month': new_month, 'new_year': new_year, 'deadline_id': deadline_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


# get deadlines in strings format
def get_deadlines_strings(user_id: int, with_ids: bool):
    list_of_deadlines = get_deadlines(user_id)
    strings = []

    for deadline in list_of_deadlines:
        if with_ids:
            strings.append(str(deadline[0]) + " " + str(deadline[1]) + ": " + str(deadline[3]) + "."
                           + str(deadline[4]) + "." + str(deadline[5]))
        else:
            strings.append(str(deadline[1]) + ": " + str(deadline[3]) + "." + str(deadline[4]) + "." + str(deadline[5]))

    return strings


def get_hot_deadlines_strings(user_id: int):
    list_of_deadlines = get_hot_deadlines(user_id)
    strings = []
    for deadline in list_of_deadlines:
        strings.append(str(deadline[1]) + ": " + str(deadline[3]) + "." + str(deadline[4]) + "." + str(deadline[5]))
    return strings


# get logs in strings format
def get_logs_strings(user_id: int):
    list_of_logs = get_logs(user_id)
    strings = []

    for log in list_of_logs:
        user_tg_name = get_user_info(log[4])[1]
        strings.append(
            "@" + user_tg_name + " - " + str(log[1]) + ", " + str(log[3]) + ", " + str(log[5]) + "."
            + str(log[6]) + "." + str(log[7]))

    return strings


# add temporarily user
def insert_tmp_user(user_id: int, tg_name: str, name: str, email: str, notifications_state: str, group_n: str,
                    code: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # insert user into tmp_users table
    cursor.execute("""INSERT INTO tmp_users 
                        (user_id, tg_name, name, group_n, email, notifications_state, code) 
                        VALUES (:user_id, :tg_name, :name, :group_n, :email, :notifications_state, :code)""",
                   {'user_id': user_id, 'tg_name': tg_name, 'name': name, 'group_n': group_n,
                    'email': email, 'notifications_state': notifications_state, 'code': code})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


def user_not_tmp_anymore(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # insert user into users table
    cursor.execute("""SELECT * FROM tmp_users WHERE user_id=:user_id""",
                   {'user_id': user_id})
    tmp_user = cursor.fetchone()
    insert_user(tmp_user[0], tmp_user[1], tmp_user[2], tmp_user[4], tmp_user[5], tmp_user[3])

    # delete user from tmp_users table
    cursor.execute("DELETE FROM tmp_users WHERE user_id=:user_id""", {'user_id': user_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


def get_code(user_id: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    # getting code
    cursor.execute("""SELECT code FROM tmp_users WHERE user_id=:user_id""",
                   {'user_id': user_id})
    code = cursor.fetchone()

    conn.close()
    return code[0]


def update_deadline_name(deadline_id: int, new_name: str):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE deadlines SET deadline_name=:new_name "
                   "WHERE id=:deadline_id;",
                   {'new_name': new_name, 'deadline_id': deadline_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0


def update_deadline_date(deadline_id: int, new_day: int, new_month: int, new_year: int):
    # connecting to the database
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE deadlines SET day=:new_day, month=:new_month, year=:new_year "
                   "WHERE id=:deadline_id;",
                   {'new_day': new_day, 'new_month': new_month, 'new_year': new_year, 'deadline_id': deadline_id})

    # save changes and disconnect db
    conn.commit()
    conn.close()
    return 0

# EXAMPLE OF USING FUNCTIONS FROM db.py IN DEADLINE-BOT

import db


def insert_user():
    user_id = int(input('Enter your user_id: '))

    tg_name = str(input('Enter your tg_name: '))

    while True:
        name = str(input('Enter your name: '))
        if len(name) > 256:
            print("Too long name. Please, try again.")
        else:
            break

    while True:
        email = str(input('Enter your email: '))
        if len(email) > 256:
            print("Too long email. Please, try again.")
        else:
            break

    check_if_email_is_correct(email)

    notifications_state = str(input("Enter your notifications_state ('on' or 'off'): "))

    while True:
        group_n = str(input('Enter your group_n in format xxxxxxx/xxxxx: '))
        if len(group_n) > 256:
            print("Too long email. Please, try again.")
        else:
            break

    check_if_group_n_is_correct(group_n)

    db.insert_user(user_id, tg_name, name, email, notifications_state, group_n)


def check_if_email_is_correct(email: str):
    pass


def check_if_group_n_is_correct(group_n: str):
    pass


def print_all_deadlines():
    user_id = int(input('Enter user_id: '))
    deadlines_for_this_group = db.get_deadlines(user_id)
    if not deadlines_for_this_group:  # if list is empty
        print("There is no deadlines for your group")
    else:
        print(deadlines_for_this_group)


def print_user_info():
    user_id = int(input('Enter user_id: '))
    user_info = db.get_user_info(user_id)
    print("your user_id: ".join(user_info[0]))
    print("your tg_name: @".join(user_info[1]))
    print("your name: ".join(user_info[2]))
    print("your group_id: ".join(user_info[3]))
    print("your email: ".join(user_info[4]))
    print("your your notifications state: ".join(user_info[5]))

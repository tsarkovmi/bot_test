import db
import sqlite3


def delete_tables():
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE users;")
    cursor.execute("DROP TABLE groups;")
    cursor.execute("DROP TABLE deadlines;")
    cursor.execute("DROP TABLE logs;")
    cursor.execute("DROP TABLE tmp_users;")
    conn.commit()
    conn.close()


def create_tables():
    conn = sqlite3.connect("database/deadline_control.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE users(
                        user_id INTEGER,
                        tg_name TEXT,
                        name TEXT,
                        group_id INTEGER,
                        email TEXT,
                        notifications_state TEXT
                        )""")

    cursor.execute("""CREATE TABLE groups(
                        id INTEGER PRIMARY KEY,
                        group_n TEXT
                        )""")

    cursor.execute("""CREATE TABLE deadlines(
                        id INTEGER PRIMARY KEY,
                        deadline_name TEXT,
                        group_id INTEGER,
                        day INTEGER,
                        month INTEGER,
                        year INTEGER
                        )""")

    cursor.execute("""CREATE TABLE logs(
                        id INTEGER PRIMARY KEY,
                        deadline_name TEXT,
                        group_id INTEGER,
                        action TEXT,
                        user_id INTEGER,
                        day INTEGER,
                        month INTEGER,
                        year INTEGER
                        )""")

    cursor.execute("""CREATE TABLE tmp_users(
                            user_id INTEGER,
                            tg_name TEXT,
                            name TEXT,
                            group_n INTEGER,
                            email TEXT,
                            notifications_state TEXT,
                            code INTEGER
                            )""")

    conn.commit()
    conn.close()


delete_tables()
create_tables()

users_list = [
    [1, "saga", "Лев", "oblomov.lo@edu.spbstu.ru", "on", "4851001/00002"],
    [2, "deadik", "Николай", "serpih.ni@edu.spbstu.ru", "on", "4851001/00002"],
    [3, "boriskashin", "Борис", "kashin.ba@edu.spbstu.ru", "on", "4851001/00001"],
    [4, "hellokek", "Геннадий", "kashin.ga@edu.spbstu.ru", "on", "4851001/00001"],
    [5, "dod", "Никита", "shlyapnikov.na@edu.spbstu.ru", "on", "4851001/00001"],
    [6, "bozhenka", "Никита", "malov.nv@edu.spbstu.ru", "on", "4851001/00003"],
    [7, "satan666", "Дарья", "shkolnikova.da@edu.spbstu.ru", "on", "4851001/00003"],
    [8, "yurich", "София", "gora.sp@edu.spbstu.ru", "on", "4851001/00003"],
    [9, "lolik", "Глеб", "kurov.gn@edu.spbstu.ru", "on", "4851001/00004"],
    [10, "bruhhhhh", "Антон", "pushkin.aa@edu.spbstu.ru", "on", "4851001/00004"],
]

deadlines_list = [
    [1, "Асвт лаба 1", 23, 3, 2022],
    [2, "Асвт лаба 2", 26, 3, 2022],
    [1, "Оси лаба 1", 30, 4, 2022],
    [2, "Курсач оси", 20, 2, 2022],
    [3, "Асвт лаба 1", 21, 3, 2022],
    [4, "Теорвер расчетка", 25, 3, 2022],
    [5, "Оси лаба 2", 28, 3, 2022],
    [6, "Контроша физика", 21, 11, 2022],
    [6, "Контроша вышмат", 30, 12, 2022],
    [9, "Комса япы", 20, 3, 2022],
    [9, "Комса схемота", 25, 3, 2022],
    [9, "Комса теорвер", 30, 3, 2022],
]

for i in range(len(users_list)):
    db.insert_user(*users_list[i])

for i in range(len(deadlines_list)):
    db.insert_deadline(*deadlines_list[i])

menu_options = {
    0: 'exit',
    1: 'add user',
    2: 'add deadline',
    3: 'delete deadline',
    4: 'all deadlines',
    5: 'hot deadlines',
    6: 'update name',
    7: 'update group',
    8: 'change notifications state',
    9: 'get user info',
    10: 'get logs',
    11: 'get all users ids',
    12: 'get_all_tg_names',
    13: 'get_deadlines_strings',
    14: 'get_logs_strings',
    15: 'insert_tmp_user',
    16: 'user_not_tmp_anymore',
    17: 'get_code',
    18: 'update_deadline_name',
    19: 'update_deadline_date'
}


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1():
    user_id = int(input('Enter your user_id: '))
    tg_name = str(input('Enter your tg_name: '))
    name = str(input('Enter your name: '))
    email = str(input('Enter your email: '))
    notifications_state = str(input('Enter your notifications_state: '))
    group_n = str(input('Enter your group_n: '))
    print('Handle option \'Option 1\'')
    db.insert_user(user_id, tg_name, name, email, notifications_state, group_n)


def option2():
    user_id = int(input('Enter your user_id: '))
    deadline_name = str(input('Enter your deadline_name: '))
    day = int(input('Enter your day: '))
    month = int(input('Enter your month: '))
    year = int(input('Enter your year: '))
    print('Handle option \'Option 2\'')
    db.insert_deadline(user_id, deadline_name, day, month, year)


def option3():
    user_id = int(input('Enter your user_id: '))
    deadline_id = int(input('Enter your deadline_id: '))
    print('Handle option \'Option 3\'')
    db.delete_deadline(user_id, deadline_id)


def option4():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 4\'')
    print(db.get_deadlines(user_id))


def option5():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 5\'')
    print(db.get_hot_deadlines(user_id))


def option6():
    user_id = int(input('Enter your user_id: '))
    new_name = str(input('Enter your new_name: '))
    print('Handle option \'Option 6\'')
    db.update_name(user_id, new_name)


def option7():
    user_id = int(input('Enter your user_id: '))
    new_group_n = str(input('Enter your new_group_n: '))
    print('Handle option \'Option 7\'')
    db.update_group(user_id, new_group_n)


def option8():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 8\'')
    db.change_notifications_state(user_id)


def option9():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 9\'')
    print(db.get_user_info(user_id))


def option10():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 10\'')
    print(db.get_logs(user_id))


def option11():
    print('Handle option \'Option 11\'')
    print(db.get_all_users_ids())


def option12():
    print('Handle option \'Option 12\'')
    print(db.get_all_tg_names())


def option13():
    user_id = int(input('Enter your user_id: '))
    with_id = input('With_id?, type True or False: ')
    if with_id == "True":
        with_id = True
    if with_id == "False":
        with_id = False
    print('Handle option \'Option 13\'')
    print(db.get_deadlines_strings(user_id, with_id))


def option14():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 14\'')
    print(db.get_logs_strings(user_id))


def option15():
    user_id = int(input('Enter your user_id: '))
    tg_name = str(input('Enter your tg_name: '))
    name = str(input('Enter your name: '))
    email = str(input('Enter your email: '))
    notifications_state = str(input('Enter your notifications_state: '))
    group_n = str(input('Enter your group_n: '))
    code = int(input('Enter your code: '))
    print('Handle option \'Option 15\'')
    db.insert_tmp_user(user_id, tg_name, name, email, notifications_state, group_n, code)


def option16():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 16\'')
    db.user_not_tmp_anymore(user_id)


def option17():
    user_id = int(input('Enter your user_id: '))
    print('Handle option \'Option 17\'')
    print(db.get_code(user_id))


def option18():
    deadline_id = int(input('Enter your deadline_id: '))
    new_name = str(input('Enter your new_name: '))
    print('Handle option \'Option 18\'')
    db.update_deadline_name(deadline_id, new_name)


def option19():
    deadline_id = int(input('Enter your deadline_id: '))
    new_day = int(input('Enter your new_day: '))
    new_month = int(input('Enter your new_month: '))
    new_year = int(input('Enter your new_year: '))
    print('Handle option \'Option 19\'')
    db.update_deadline_date(deadline_id, new_day, new_month, new_year)


if __name__ == '__main__':
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 0:
            print('Thanks message before exiting')
            exit()
        elif option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            option6()
        elif option == 7:
            option7()
        elif option == 8:
            option8()
        elif option == 9:
            option9()
        elif option == 10:
            option10()
        elif option == 11:
            option11()
        elif option == 12:
            option12()
        elif option == 13:
            option13()
        elif option == 14:
            option14()
        elif option == 15:
            option15()
        elif option == 16:
            option16()
        elif option == 17:
            option17()
        elif option == 18:
            option18()
        elif option == 19:
            option19()
        else:
            print('Invalid option. Please enter a number between 0 and 19.')

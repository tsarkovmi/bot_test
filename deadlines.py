from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import dp, Bot, bot, main_keyboard
import datetime
from database.db import get_deadlines_strings, get_hot_deadlines_strings, delete_deadline, insert_deadline, \
    update_deadline_date, update_deadline_name


class FSMdeadline(StatesGroup):
    deadline_name = State()
    deadline_date = State()
    deadline_delete = State()
    changeind_choice = State()
    changeparam_choice = State()
    change_name = State()
    change_date = State()


name = 'sss'
date = []
deadlines_index = []
changed_id = 0
changed_deadline = 'ggg'


def get_index(user_id):
    deadline_list = get_deadlines_strings(user_id, True)
    global deadlines_index
    deadlines_index = []
    for item in deadline_list:
        numb = []
        for i in range(5):
            if item[i] == ' ':
                break
            else:
                numb.append(item[i])
        aded_elem = int(''.join(map(str, numb)))
        deadlines_index.append(aded_elem)


@dp.message_handler(commands=['CreateDeadline'])
async def create_deadline(message: types.Message):
    await bot.send_message(message.from_user.id, "Введи название дедлайна")
    await FSMdeadline.deadline_name.set()


@dp.message_handler(state=FSMdeadline.deadline_name)
async def deadline_name(message: types.Message):
    global name
    name = message.text
    await FSMdeadline.next()
    await bot.send_message(message.from_user.id, "Теперь введи дату дедлайна в формате дд.мм.гггг")


@dp.message_handler(state=FSMdeadline.deadline_date)
async def deadline_date(message: types.Message, state: FSMContext):
    global date
    triger = 0
    str_date = message.text
    date = str_date.split(".")
    current_date = datetime.datetime.now()
    year=int(date[2])
    month=int(date[1])
    day=int(date[0])
    if day>31 or month>12:
        await bot.send_message(message.from_user.id, "Эта дата никогда не наступит, введи другую дату дедлайна "
                                                     "в формате дд.мм.гггг")
    else:
        deadline_dat = datetime.datetime(year,month,day)
        difference = (deadline_dat - current_date).days
        if difference<0:
            await bot.send_message(message.from_user.id, "Ты не можешь добавлять прошедшие дедлайны, введи дату дедлайна "
                                                         "в формате дд.мм.гггг")

        else:
            if len(date) != 3:
                await bot.send_message(message.from_user.id, "Неверный формат ввода, введи дату дедлайна в формате дд.мм.гггг")
            else:
                for i in date:
                    if not i.isdigit():
                        triger = 1
                if triger == 0:
                    await bot.send_message(message.from_user.id,
                                           f"Добавлен дедлайн {name} на {int(date[0])}.{int(date[1])}.{int(date[2])}",
                                           reply_markup=main_keyboard)
                    insert_deadline(message.from_user.id, name, int(date[0]), int(date[1]), int(date[2]))
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id,
                                           "Неверный формат ввода, введи дату дедлайна в формате дд.мм.гггг")


@dp.message_handler(commands=['All_deadlines'])
async def all_deadlines(message: types.Message):
    deadline_list = get_deadlines_strings(message.from_user.id, False)
    await bot.send_message(message.from_user.id, "Вот список всех дедлайнов у вашей группы")
    await bot.send_message(message.from_user.id, '\n'.join(deadline_list), reply_markup=main_keyboard)


# вывод дедлайнов до которых меньше недели
@dp.message_handler(commands=['Hot_deadline'])
async def hot_deadlines(message: types.Message):
    deadline_list = get_hot_deadlines_strings(message.from_user.id)
    await bot.send_message(message.from_user.id, f"У вас горят следующие дедлайны:")
    await bot.send_message(message.from_user.id, '\n'.join(deadline_list), reply_markup=main_keyboard)


@dp.message_handler(commands=['DeleteDeadline'])
async def delete_deadline_func(message: types.Message):
    await FSMdeadline.deadline_delete.set()
    deadline_list = get_deadlines_strings(message.from_user.id, True)
    get_index(message.from_user.id)
    await bot.send_message(message.from_user.id, "Вот список всех дедлайнов у вашей группы\n "
                                                 "введи номер дедлайна который ты хочешь удалить")
    await bot.send_message(message.from_user.id, '\n'.join(deadline_list))


@dp.message_handler(state=FSMdeadline.deadline_delete)
async def delete_choice(message: types.Message, state: FSMContext):
    try:
        mes_code = int(message.text)
    except ValueError:
        await bot.send_message(message.from_user.id,
                               f'Что-то не то, дедлайна с таким номером нет, попробуй ещё раз')
    else:
        if int(message.text) in deadlines_index:
            delete_deadline(message.from_user.id, int(message.text))
            await bot.send_message(message.from_user.id, f"дедлайн удалён", reply_markup=main_keyboard)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id,
                                   f'Что-то не то, дедлайна с таким номером нет, попробуй ещё раз')


@dp.message_handler(commands=['ChangeDeadline'])
async def change_deadline(message: types.Message):
    await FSMdeadline.changeind_choice.set()
    deadline_list = get_deadlines_strings(message.from_user.id, True)
    get_index(message.from_user.id)
    await bot.send_message(message.from_user.id, "Вот список всех дедлайнов у вашей группы\n "
                                                 "введи номер дедлайна который ты хочешь изменить")
    await bot.send_message(message.from_user.id, '\n'.join(deadline_list))


@dp.message_handler(state=FSMdeadline.changeind_choice)
async def for_choice_deadle(message: types.Message, state: FSMContext):
    global changed_deadline
    global changed_id
    try:
        mes_code = int(message.text)
    except ValueError:
        await bot.send_message(message.from_user.id,
                               f'Что-то не то, дедлайна с таким номером нет, попробуй ещё раз')
    else:
        if int(message.text) in deadlines_index:
            await FSMdeadline.changeparam_choice.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = ["Название", "Дату"]
            keyboard.add(*buttons)
            changed_id = message.text
            await bot.send_message(message.from_user.id, "Что хотите изменить?", reply_markup=keyboard)
        else:
            await bot.send_message(message.from_user.id,
                                   f'Что-то не то, дедлайна с таким номером нет, попробуй ещё раз')


@dp.message_handler(Text(equals="Дату"), state=FSMdeadline.changeparam_choice)
async def new_deadline_date(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите новую дату в формате дд.мм.гггг\n')
    await FSMdeadline.change_date.set()


@dp.message_handler(state=FSMdeadline.change_date)
async def new_date(message: types.Message, state: FSMContext):
    global date
    global changed_deadline
    triger = 0
    str_date = message.text
    date = str_date.split(".")
    if len(date) != 3:
        await bot.send_message(message.from_user.id, "Неверный формат ввода, введи дату дедлайна в формате дд.мм.гггг")
    else:
        for i in date:
            if not i.isdigit():
                triger = 1
        if triger == 0:
            await bot.send_message(message.from_user.id,
                                   f"Дата дедлайна изменена на {int(date[0])}.{int(date[1])}.{int(date[2])}",
                                   reply_markup=main_keyboard)
            update_deadline_date(int(changed_id), int(date[0]), int(date[1]), int(date[2]),message.from_user.id)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id,
                                   "Неверный формат ввода, введи дату дедлайна в формате дд.мм.гггг",
                                   reply_markup=main_keyboard)


@dp.message_handler(Text(equals="Название"), state=FSMdeadline.changeparam_choice)
async def new_deadline_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите новое название\n')
    await FSMdeadline.change_name.set()


@dp.message_handler(state=FSMdeadline.change_name)
async def new_name(message: types.Message, state: FSMContext):
    update_deadline_name(changed_id, message.text,message.from_user.id)
    await bot.send_message(message.from_user.id, f'Имя дедлайна изменено на {message.text}\n',
                           reply_markup=main_keyboard)
    await state.finish()


def deadlines_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_deadline_func, commands='DeleteDeadline')
    dp.register_message_handler(change_deadline, commands='ChangeDeadline')
    dp.register_message_handler(create_deadline, commands='CreateDeadline')
    dp.register_message_handler(hot_deadlines, commands='Hot_deadline')
    dp.register_message_handler(all_deadlines, commands='All_deadlines')

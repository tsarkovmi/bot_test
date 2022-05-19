import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot, dp, dat, main_keyboard
from database.db import insert_user, insert_tmp_user, get_code, user_not_tmp_anymore
from auth.auth import auth
from random import randint

group_numb = "1"
mail = "1"


class FSMdata(StatesGroup):
    group = State()
    mail = State()
    name = State()
    code = State()


async def start_func(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, я бот который будет напоминать тебе о дедлайнах, чтобы ты '
                                                 'сдавал все работы вовремя')
    await bot.send_message(message.from_user.id, 'Для начала введи свою группу в формате\n'
                                                 ' nnnnnnn/nnnnn')
    await FSMdata.group.set()


@dp.message_handler(state=FSMdata.group)
async def group(message: types.Message):
    global group_numb
    await FSMdata.group.set()
    group_numb = message.text
    await FSMdata.next()
    await bot.send_message(message.from_user.id, 'Введи свою корпоративную почту\n(которая ...@edu.spbstu.ru)')


@dp.message_handler(state=FSMdata.mail)
async def mail_addres(message: types.Message, state: FSMContext):
    global mail
    mail = message.text
    test_mail = "@edu.spbstu.ru"
    if test_mail in mail:
        await FSMdata.next()
        await bot.send_message(message.from_user.id, f'Осталось выяснить как тебя зовут {message.from_user.username}')
    else:
        await bot.send_message(message.from_user.id, 'Формат почты не ...@edu.spbstu.ru \n попробуй ещё раз')


@dp.message_handler(state=FSMdata.name)
async def username(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.text
    tg_name = message.from_user.username
    auth_code = random.randint(111111, 999999)
    await bot.send_message(message.from_user.id,
                           f'{tg_name}, на твою почту придёт письмо с кодом регистрации, введи его следующим '
                           f'сообщением и получишь доступ ко всем функциям.')
    auth(mail, str(auth_code))
    insert_tmp_user(user_id, tg_name, user_name, mail, 'on', group_numb, auth_code)
    await FSMdata.next()


@dp.message_handler(state=FSMdata.code)
async def code_wait(message: types.Message, state: FSMContext):
    right_code = get_code(message.from_user.id)
    try:
        mes_code = int(message.text)
    except ValueError:
        await bot.send_message(message.from_user.id,
                               f'Что-то не то, у нас записан другой код, попробуй ещё раз')
    else:
        if int(message.text) == right_code:
            await bot.send_message(message.from_user.id,
                                   f'отлично! теперь ты можешь начинать пользоваться ботом. Все его функции ты можешь '
                                   f'узнать по команде /help',
                                   reply_markup=main_keyboard)
            user_not_tmp_anymore(message.from_user.id)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id,
                                   f'Что-то не то, у нас записан другой код, попробуй ещё раз')



def user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_func, commands='start')
    dp.register_message_handler(mail_addres, state=FSMdata.mail)
    dp.register_message_handler(username, state=FSMdata.name)

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


BOT_TOKEN = os.getenv('5212835004:AAGmJU-DyQeYaDlW7Xr8lEzHI5ew7U7cB2g')
if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

HEROKU_APP_NAME = os.getenv('botdeadline-test')


# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))

dat = MemoryStorage()
bot = Bot(token='5212835004:AAGmJU-DyQeYaDlW7Xr8lEzHI5ew7U7cB2g')
dp = Dispatcher(bot, storage=dat)


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/Help')
b2 = KeyboardButton('/CreateDeadline')
b3 = KeyboardButton('/ChangeDeadline')
b4 = KeyboardButton('/Settings')
b5 = KeyboardButton('/Hot_deadline')
b6 = KeyboardButton('/All_deadlines')
b7 = KeyboardButton('/DeleteDeadline')
b8 = KeyboardButton('/Logs')
main_keyboard.add(b1, b3)
main_keyboard.row(b5, b6)
main_keyboard.row(b2, b7)
main_keyboard.row(b8, b4)

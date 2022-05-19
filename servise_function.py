from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot, dp, main_keyboard
from database.db import get_logs_strings, update_name, update_group, change_notifications_state, get_user_info

User_name = "default"
User_group = "0000000/00000"


class FSMsettings(StatesGroup):
    setting_type = State()
    name_change = State()
    group_change = State()
    notification_change = State()


async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'КОМАНДЫ БОТА\n'
                                                 '/CreateDeadline – добавить дедлайн\n'
                                                 '/ChangeDeadline – изменить дату дедлайна\n'
                                                 '/DeleteDeadline - удалить дедлайн из списка\n'
                                                 '/Settings – изменить номер группы или имя или включить/отключить '
                                                 'уведомления\n '
                                                 '/Logs - позволяет посмотреть кто, когда и как менял дедлайны твоей '
                                                 'группы\n '
                                                 '/Hot_deadline – показывает дедлайны, до которых меньше недели\n'
                                                 '/All_deadlines - показывает все дедлайны вашей группы\n'
                                                 '', reply_markup=main_keyboard)


@dp.message_handler(commands=['Settings'])
async def userinfo_settings(message: types.Message):
    await FSMsettings.setting_type.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Группу", "Имя", "Параметры уведомлений"]
    keyboard.add(*buttons)
    await bot.send_message(message.from_user.id, "Что хотите изменить?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Группу"), state=FSMsettings.setting_type)
async def change_group_func(message: types.Message, state: FSMContext):
    # Тут место для ввода нового номера группы с помощью функции которая вначале будет проверять корректность номера
    # группы
    await bot.send_message(message.from_user.id, 'Введите новую группу\n')
    await FSMsettings.group_change.set()


@dp.message_handler(Text(equals="Имя"), state=FSMsettings.setting_type)
async def change_name_func(message: types.Message, state: FSMContext):
    # Тут место для ввода нового логина с помощью функции которая вначале будет проверять не существует ли уже логин
    await bot.send_message(message.from_user.id, 'Введите новое имя\n')
    await FSMsettings.name_change.set()


@dp.message_handler(state=FSMsettings.name_change)
async def newname(message: types.Message, state: FSMContext):
    update_name(message.from_user.id, message.text)
    await state.finish()
    await bot.send_message(message.from_user.id, f"Ваше имя успешно изменено на {message.text}",
                           reply_markup=main_keyboard)


@dp.message_handler(state=FSMsettings.group_change)
async def newgroup(message: types.Message, state: FSMContext):
    update_group(message.from_user.id, message.text)
    await state.finish()
    await bot.send_message(message.from_user.id, f"Ваша группа успешно изменена на {message.text}",
                           reply_markup=main_keyboard)


@dp.message_handler(Text(equals="Параметры уведомлений"), state=FSMsettings.setting_type)
async def change_notification_settings(message: types.Message, state: FSMContext):
    change_notifications_state(message.from_user.id)
    user_info = get_user_info(message.from_user.id)
    if user_info[5] == 'on':
        await bot.send_message(message.from_user.id, 'Уведомлений успешно включены\n',
                               reply_markup=main_keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Уведомлений успешно отключены\n',
                               reply_markup=main_keyboard)
    await state.finish()


# получить логи по своей группе
async def logs_output(message: types.Message):
    await bot.send_message(message.from_user.id, "Логи вашей группы:")
    # logs_list = get_logs(message.from_user.id)
    # await bot.send_message(message.from_user.id, logs_list,
    #                         reply_markup=main_keyboard)
    logs_list = get_logs_strings(message.from_user.id)
    await bot.send_message(message.from_user.id, '\n'.join(logs_list),
                           reply_markup=main_keyboard)


# инфа о боте
async def about_bot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Бот, который следит за дедлайнами вместо Вас!\n'
                                                 'Вы можете добавлять новые дедлайны или изменять дату существующих.\n'
                                                 'Бот напомнит Вам о подходящем дедлайне (за 7 и за 2 дня до его '
                                                 'окончания).\n '
                                                 'Также при внесении изменении Вам будет приходить оповещение,\n'
                                                 'сообщающее о том, что изменилось и кто внес изменение.\n'
                                                 'При необходимости бот может вывести как все дедлайны сразу,\n'
                                                 'так и по конкретному предмету.\n')


def settings_handlers(dp: Dispatcher):
    dp.register_message_handler(help_command, commands='Help')
    dp.register_message_handler(logs_output, commands='Logs')
    dp.register_message_handler(userinfo_settings, commands='Settings')

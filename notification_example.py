#  Это пример бота с использованием рассылки уведомлений.
#  Важный код выделен так > ##################################

from telegram.ext import Updater, CommandHandler
import logging
from database import db
################################
from notifications import schedule_notifications
################################

updater = Updater(token='5165160034:AAE6gKPi-JE1gJpSGgFSF15pDNAw5A9h0bg', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# writing functionality of the command
def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    db.insert_user(user_id, user_name, "Имя", "dfa@ya.ru", "on", "4851001/00002")


# give a name to the command and add it to the dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

####################################
schedule_notifications(updater)
##########################################
updater.start_polling()  # enable bot to get updates
updater.idle()

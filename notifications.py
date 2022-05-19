# NOTIFICATION FUNCTION
from telegram.ext import CallbackContext
from database import db
import datetime


def send_notifications(context: CallbackContext):
    # send message to all users
    users_ids = db.get_all_users_ids()
    for u_id in users_ids:
        user_notif_state = db.get_user_info(u_id[0])[5]
        if user_notif_state == 'on':
            message = "Your deadlines:\n" + str(db.get_deadlines(u_id[0]))
            context.bot.send_message(chat_id=u_id[0], text=message)


def schedule_notifications(updater):
    job = updater.job_queue
    job_daily = job.run_daily(send_notifications, days=(0, 1, 2, 3, 4, 5, 6),
                              time=datetime.time(hour=7, minute=00, second=00))  # time in UTC (10:00 moscow)

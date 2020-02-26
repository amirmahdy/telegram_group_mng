# coding=utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import memcache
import telegram
import re
import time
from config import *
from model import *

CHOOSING, TYPING_SLP, TYPING_WAK, NAME_ENTERY, PLACE_ENTRY, COMPLETE_ENTRY = range(12)
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=True)

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
dbot = telegram.Bot(BOT_TOKEN)


def start(update, context):
    custom_keyboard = [[REGISTER_BTN]]
    newmarkup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    update.message.reply_text(WELCOME_MSG, reply_markup=newmarkup)
    return NAME_ENTERY


def nameentry(update, context):
    update.message.reply_text(ENTER_NAME)
    return PLACE_ENTRY


def placeentry(update, context):
    text = update.message.text
    data[str(update.message.from_user.id) + 'name'] = text
    update.message.reply_text(ENTER_PLACE)
    return COMPLETE_ENTRY


def completeentry(update, context):
    text = update.message.text
    data[str(update.message.from_user.id) + 'place'] = text
    try:
        register_user(update.message.from_user.id, data[str(update.message.from_user.id) + 'name'], data[str(update.message.from_user.id) + 'place'])
    except Exception as e:
        if str(update.effective_user.id) in admins:
            update.message.reply_text(ACCOUNT_EXISTS, reply_markup=admin_markup)
            return CHOOSING

    if str(update.effective_user.id) in admins:
        update.message.reply_text(ACCOUNT_SUCCESS, reply_markup=admin_markup)

    return CHOOSING


def adduser(user_id, admin):
    if admin == 1:
        file = open('group_admin.csv', "a+")

    file.writelines(str(user_id) + '\n')
    file.close()


def removeuser(user_id, admin):
    if admin == 1:
        filename = "group_admin.csv"

    with open(filename, "r") as f:
        lines = f.readlines()
        f.close()
    with open(filename, "w") as f:
        for line in lines:
            if line.strip() != user_id:
                f.write(line)
    f.close()


def but_menu(update, context):
    text = update.message.text
    status = dbot.get_chat_member(Group_ID, update.effective_user.id).status
    user_id = str(update.effective_user.id)
    if status == 'administrator' or 'creator':
        if user_id not in admins:
            admins.append(user_id)
            adduser(user_id, 1)
        elif user_id in users:
            users.remove(user_id)
            removeuser(user_id, 0)

        if text == BACK_BTN:
            update.message.reply_text(MAIN_MENU, reply_markup=admin_markup)
            return CHOOSING
        if text == HOME_BTN:
            update.message.reply_text(rules, reply_markup=admin_markup)
            return CHOOSING


def done(update, context):
    return ConversationHandler.END


def newmember(update, context):
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    dbot.delete_message(chat_id, msg_id)
    dbot.send_message(chat_id, update.message.from_user.id.full_name + WELCOME_MSG, disable_notification=True)


def leftmember(update, context):
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    dbot.delete_message(chat_id, msg_id)


def msg_handle(update, context):
    text = update.message.text
    tm = time.localtime().tm_hour
    if str(update.effective_user.id) not in admins:
        if sleep_tm <= tm or wake_tm > tm or re.search(text_rules, text) or group_active == 0:
            chat_id = update.message.chat_id
            msg_id = update.message.message_id
            dbot.delete_message(chat_id, msg_id)


def sleep_time(update, context):
    if str(update.effective_user.id) in admins:
        update.message.reply_text(SLEEP_MSG)
        return TYPING_SLP
    else:
        return CHOOSING


def sleep_set(update, context):
    global sleep_tm
    if str(update.effective_user.id) in admins:
        text = update.message.text
        sleep_tm = int(text)
        callback_timer(update, context)
    return CHOOSING


def wake_time(update, context):
    if str(update.effective_user.id) in admins:
        update.message.reply_text(WAKE_MSG)
        return TYPING_WAK
    else:
        return CHOOSING


def wake_set(update, context):
    global wake_tm
    if str(update.effective_user.id) in admins:
        text = update.message.text
        wake_tm = int(text)
        wake_callback_timer(update, context)
    return CHOOSING


def group_stop(update, context):
    global group_active
    if group_active == 1:
        group_active = 0
        update.message.reply_text(GROUP_STOP_MSG)
    else:
        group_active = 1
        update.message.reply_text(GROUP_START_MSG)


def callback_alarm(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=Group_ID, text=MSG_TO_GROUP_STOP)


def callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    global job_minute
    if job_minute is not None:
        job_minute.schedule_removal()
    current_time = time.localtime().tm_hour * 3600 + time.localtime().tm_min * 60 + time.localtime().tm_sec
    expected_time = sleep_tm * 3600
    if expected_time > current_time:
        starttime = expected_time - current_time
    else:
        starttime = 86400 + expected_time - current_time

    job_minute = j.run_repeating(callback_alarm, 86400, starttime, context=update.message.chat_id)


def wake_callback_alarm(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=Group_ID, text=MSG_TO_GROUP_START)


def wake_callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    global wake_job_minute
    if wake_job_minute is not None:
        wake_job_minute.schedule_removal()
    current_time = time.localtime().tm_hour * 3600 + time.localtime().tm_min * 60 + time.localtime().tm_sec
    expected_time = wake_tm * 3600
    if expected_time > current_time:
        starttime = expected_time - current_time
    else:
        starttime = 86400 + expected_time - current_time

    wake_job_minute = j.run_repeating(wake_callback_alarm, 86400, starttime, context=update.message.chat_id)


updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
j = updater.job_queue
job_minute = None
wake_job_minute = None

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.regex('^(' + ADMIN_SLEEP_BTN + ')$'), sleep_time),
                  MessageHandler(Filters.regex('^(' + ADMIN_WAKE_BTN + ')$'), wake_time), MessageHandler(Filters.regex('^(' + ADMIN_STOP_BTN + ')$'), group_stop),
                  MessageHandler(Filters.regex('^(' + REGISTER_BTN + ')$'), nameentry)],

    states={  # Creating the main menu
        CHOOSING: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.regex('^(' + ADMIN_SLEEP_BTN + ')$'), sleep_time),
                   MessageHandler(Filters.regex('^(' + ADMIN_WAKE_BTN + ')$'), wake_time), MessageHandler(Filters.regex('^(' + ADMIN_STOP_BTN + ')$'), group_stop),
                   MessageHandler(Filters.regex('^(' + REGISTER_BTN + ')$'), nameentry)],
        TYPING_SLP: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.text, sleep_set)],
        TYPING_WAK: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.text, wake_set)],
        NAME_ENTERY: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.text, nameentry)],
        PLACE_ENTRY: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.text, placeentry)],
        COMPLETE_ENTRY: [MessageHandler(Filters.regex('^((' + BACK_BTN + ')|(' + HOME_BTN + '))$'), but_menu), MessageHandler(Filters.text, completeentry)]}, fallbacks=[CommandHandler('stop', done)])

dp.add_handler(conv_handler)
dp.add_handler(MessageHandler(Filters.chat(Group_ID) & Filters.status_update.new_chat_members, newmember))
dp.add_handler(MessageHandler(Filters.chat(Group_ID) & Filters.status_update.left_chat_member, leftmember))
dp.add_handler(MessageHandler(Filters.chat(Group_ID) & Filters.text, msg_handle))
dp.add_handler(CommandHandler('start', start, filters=~Filters.chat(Group_ID)))

updater.start_polling()
updater.idle()

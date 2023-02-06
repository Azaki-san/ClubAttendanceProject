import lang
import telebot
from working_with_db import WorkingWithDB, dbClone
from work_functions import returnAllClubsKeyboard


def general(message, bot, LANG, clubID):
    msg = message.text
    if msg == lang.adminFirst[LANG]['editingDescription']:
        editingClubInfo(message, bot, LANG, clubID)
    elif msg == lang.adminFirst[LANG]['deletingClub']:
        confirmingDeleting(message, bot, LANG, clubID)


def confirmingDeleting(message, bot, LANG, clubID):
    userID = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
    btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['confirm'])
    markup.add(btn2, btn1)
    msg = bot.send_message(userID, lang.adminFirst[LANG]["confirmingDeleting"], reply_markup=markup)
    bot.register_next_step_handler(msg, deleting, bot, LANG, clubID)


def deleting(message, bot, LANG, clubID):
    confirming = message.text
    userID = message.chat.id
    if confirming == lang.adminFirst[LANG]['confirm']:
        dbClone.remove_club(clubID)
        bot.send_message(userID,
                     text=f'{lang.adminFirst[LANG]["successfulClubDeleting"]}\n{lang.adminFirst[LANG]["all_clubs"]}',
                     reply_markup=returnAllClubsKeyboard(LANG))
    elif confirming == lang.adminFirst[LANG]["cancel"]:
        bot.send_message(userID,
                         text=f'{lang.adminFirst[LANG]["cancelledDeleting"]}\n{lang.adminFirst[LANG]["all_clubs"]}',
                         reply_markup=returnAllClubsKeyboard(LANG))

def editingClubInfo(clubID):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
    btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['editingDescription'])
    btn3 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['editingDescription'])
    btn4 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['editingDescription'])
    btn5 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['editingDescription'])
    print(clubID)

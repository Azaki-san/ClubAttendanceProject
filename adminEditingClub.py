import telebot

import lang
from work_functions import returnAllClubsKeyboard, printingDescription
from working_with_db import WorkingWithDB, dbClone


def general(message, bot, LANG, clubID):
    msg = message.text
    userID = message.chat.id
    if msg == lang.adminFirst[LANG]['editingDescription']:
        editingClubInfo(message, bot, LANG, clubID)
    elif msg == lang.adminFirst[LANG]['deletingClub']:
        confirmingDeleting(message, bot, LANG, clubID)
    elif msg == lang.adminFirst[LANG]['back']:
        bot.send_message(userID,
                         text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))


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
                         text=lang.adminFirst[LANG]["successfulClubDeleting"])
        bot.send_message(userID,
                         text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))
    elif confirming == lang.adminFirst[LANG]["cancel"]:
        bot.send_message(userID,
                         text=lang.adminFirst[LANG]["cancelledDeleting"])
        bot.send_message(userID,
                         text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))


def editingClubInfo(message, bot, LANG, clubID):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    userID = message.chat.id
    btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['nameOfTheClub'])
    btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['clubHeads'])
    btn3 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['amountOfMeetings'])
    btn4 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['clubDescription'])
    btn5 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['photoLogo'])
    btn6 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    msg = bot.send_message(userID, lang.adminFirst[LANG]["choiceOfEditing"], reply_markup=markup)
    bot.register_next_step_handler(msg, editing, bot, LANG, clubID)


def editing(message, bot, LANG, clubID):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    choice = message.text
    userID = message.chat.id
    btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
    markup.add(btn1)
    if choice == lang.adminFirst[LANG]["clubHeads"]:
        msg = bot.send_message(userID, text=lang.adminFirst[LANG]["addHeadClub"],
                               parse_mode='Markdown', reply_markup = markup)
        bot.register_next_step_handler(msg, changingDataOfTheClub, bot, LANG, clubID, choice)
    elif choice == lang.adminFirst[LANG]["cancel"]:
        bot.send_message(userID,
                         text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))
    elif choice == lang.adminFirst[LANG]["nameOfTheClub"] or choice == lang.adminFirst[LANG]["amountOfMeetings"] or choice == lang.adminFirst[LANG]["clubDescription"]:
        msg = bot.send_message(userID, lang.adminFirst[LANG]["enteringNewData"], reply_markup = markup)
        bot.register_next_step_handler(msg, changingDataOfTheClub, bot, LANG, clubID, choice)
    else:
        msg = bot.send_message(userID, lang.adminFirst[LANG]["tryAgain"], reply_markup=markup)
        editingClubInfo(msg, bot, LANG, clubID)


def changingDataOfTheClub(message, bot, LANG, clubID, type):
    data = message.text
    userID = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if data != 'Back':
        if type == lang.adminFirst[LANG]['nameOfTheClub']:
            dbClone.change_name_of_club(data, clubID)
        elif type == lang.adminFirst[LANG]['clubHeads']:
            head_club = data.split()
            head_club_ids = []
            fileWithQueue = open("queue.txt", 'r+')
            strQueue = fileWithQueue.read()
            print(strQueue)
            queue = eval(strQueue)
            for i in head_club:
                exist = dbClone.is_exist(i)
                if exist != -1:
                    head_club_ids.append(eval(exist)[0])
                else:
                    if queue.get(i):
                        queue[i].append(dbClone.get_next_club_id())
                    else:
                        queue[i] = [dbClone.get_next_club_id()]
            fileWithQueue.seek(0)
            fileWithQueue.write(str(queue))
            dbClone.update_leaders(str(head_club_ids), clubID)
        elif type == lang.adminFirst[LANG]['amountOfMeetings']:
            dbClone.change_amount_of_meetings(data, clubID)
        elif type == lang.adminFirst[LANG]['clubDescription']:
            dbClone.add_a_description(data, clubID)
        elif type == lang.adminFirst[LANG]['photoLogo']:
            msg = bot.send_message(userID, text=lang.adminFirst[LANG]["addPhoto"])
            bot.register_next_step_handler(msg, changingPhoto)
        msg = bot.send_message(userID, text=lang.adminFirst[LANG]["successfulEdition"],
                               parse_mode='Markdown')
        bot.send_message(userID, text=printingDescription(LANG, dbClone.return_club_by_id(clubID)[0]),
                               parse_mode='Markdown', reply_markup=markup)
        editingClubInfo(message, bot, LANG, clubID)
    else:
        editingClubInfo(message, bot, LANG, clubID)


import telebot

import lang
from work_functions import returnAllClubsKeyboard, dbClone, printingDescription, getParsedAliases


# СДЕЛАТЬ КНОПКУ НАЗАД ИЛИ ЧТО-ТО ПОДОБНОЕ
# СДЕЛАТЬ ПЕРЕХОД В СПИСОК ВСЕХ КЛУБОВ В ПОСЛЕДНЕЙ ФУНКЦИИ

def nado(LANG, name_club, head_club, meeting_count):
    finalString = f""
    listOfAliases = head_club.split()
    finalString = f"***{lang.adminFirst[LANG]['nameOfTheClub']}***: {name_club}\n***{lang.adminFirst[LANG]['clubHeads']}***: "
    finalString += getParsedAliases(listOfAliases) + '\n'
    finalString += f"***{lang.adminFirst[LANG]['clubDescription']}***: {lang.adminFirst[LANG]['willAdd']}\n"
    finalString += f"***{lang.adminFirst[LANG]['photoLogo']}***: {lang.adminFirst[LANG]['willAdd']}\n"
    finalString += f"***{lang.adminFirst[LANG]['amountOfMeetings']}***: {meeting_count}\n"
    return finalString


def addNameClub(message, bot, LANG):
    userID = message.chat.id
    name_club = message.text
    if name_club == lang.adminFirst[LANG]['cancel']:
        bot.send_message(userID, lang.adminFirst[LANG]["addClubCancel"])
        bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2)
        msg = bot.send_message(userID, lang.adminFirst[LANG]["addHeadClub"], reply_markup=markup)
        bot.register_next_step_handler(msg, addHeadClub, bot, LANG, name_club)


def addHeadClub(message, bot, LANG, name_club):
    userID = message.chat.id
    """Тут нужно подумать что принимать: алиас или еще какую-нибудь хрень."""
    head_club = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if head_club == lang.adminFirst[LANG]['cancel']:
        bot.send_message(userID, lang.adminFirst[LANG]["addClubCancel"])
        bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))
    elif head_club == lang.adminFirst[LANG]['back']:
        btn = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        markup.add(btn)
        msg = bot.send_message(userID, text=lang.adminFirst[LANG]["addNameClub"], reply_markup=markup)
        bot.register_next_step_handler(msg, addNameClub, bot, LANG)
    else:
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2)
        msg = bot.send_message(userID, lang.adminFirst[LANG]["addClubMeetingCount"], reply_markup=markup)
        bot.register_next_step_handler(msg, addClubMeetingCount, bot, LANG, name_club, head_club)


def addClubMeetingCount(message, bot, LANG, name_club, head_club):
    userID = message.chat.id
    # СДЕЛАТЬ ПРОВЕРКУ НА INT
    meeting_count = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    checkingIfInt = 0
    try:
        a = int(meeting_count)
    except Exception:
        if meeting_count != lang.adminFirst[LANG]['back'] and meeting_count != lang.adminFirst[LANG]['cancel']:
            checkingIfInt = 1

    '''Возможно это стоит вынести в отдельную функцию'''
    if meeting_count == lang.adminFirst[LANG]['cancel']:
        bot.send_message(userID, lang.adminFirst[LANG]["addClubCancel"])
        bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))
    elif meeting_count == lang.adminFirst[LANG]['back'] or checkingIfInt:
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2)
        text2 = lang.adminFirst[LANG]["addHeadClub"]
        if checkingIfInt:
            text2 = lang.adminFirst[LANG]["wrongData"]
            msg = bot.send_message(userID, text=text2, reply_markup=markup)
            bot.register_next_step_handler(msg, addClubMeetingCount, bot, LANG, name_club, head_club)
        else:
            msg = bot.send_message(userID, text=text2, reply_markup=markup)
            bot.register_next_step_handler(msg, addHeadClub, bot, LANG, name_club)
    else:
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['confirm'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        btn3 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2, btn3)
        # msg = bot.send_message(userID, printingDescription(LANG, [0, name_club, str(head_club.split()), meeting_count]), reply_markup=markup)
        final_string = nado(LANG, name_club, head_club, meeting_count)
        print(final_string)
        msg = bot.send_message(userID, f"{final_string}Confirm?", reply_markup=markup, parse_mode="MarkdownV2")

        bot.register_next_step_handler(msg, addClubConfirmation, bot, LANG, name_club, head_club, meeting_count)


def addClubConfirmation(message, bot, LANG, name_club, head_club, meeting_count):
    userID = message.chat.id
    confirmation = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if confirmation == lang.adminFirst[LANG]['confirm']:
        head_club = head_club.split()
        head_club_ids = []
        fileWithQueue = open("queue.txt", 'r+')
        strQueue = fileWithQueue.read()
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
        print(head_club_ids)
        success = dbClone.create_new_club(name_club, meeting_count, head_club_ids)

        # здесь должна быть попытка обновить базу данных
        if success:  # если успех, то
            bot.send_message(userID, lang.adminFirst[LANG]["addClubSuccess"])
            bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                             reply_markup=returnAllClubsKeyboard(LANG))
            '''отправить в call значение, чтобы вернуть админа к списку клубов. почитать как это сделать,
            возможно пусть коля этим занимается'''
        else:  # не успех
            bot.send_message(userID, lang.adminFirst[LANG]['addClubFailed'])
    elif confirmation == lang.adminFirst[LANG]['back']:
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2)
        msg = bot.send_message(userID, text=lang.adminFirst[LANG]["addClubMeetingCount"], reply_markup=markup)
        bot.register_next_step_handler(msg, addClubMeetingCount, bot, LANG, name_club, head_club)
    else:
        bot.send_message(userID, lang.adminFirst[LANG]["addClubCancel"])
        bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                         reply_markup=returnAllClubsKeyboard(LANG))

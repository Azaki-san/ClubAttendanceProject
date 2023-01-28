import lang
import telebot
from work_functions import returnAllClubsKeyboard


# СДЕЛАТЬ КНОПКУ НАЗАД ИЛИ ЧТО-ТО ПОДОБНОЕ
# СДЕЛАТЬ ПЕРЕХОД В СПИСОК ВСЕХ КЛУБОВ В ПОСЛЕДНЕЙ ФУНКЦИИ
def addNameClub(message, bot, LANG):
    userID = message.chat.id
    name_club = message.text

    msg = bot.send_message(userID, lang.adminFirst[LANG]["addHeadClub"])
    bot.register_next_step_handler(msg, addHeadClub, bot, LANG, name_club)


def addHeadClub(message, bot, LANG, name_club):
    userID = message.chat.id
    """Тут нужно подумать что принимать: алиас или еще какую-нибудь хрень."""
    head_club = message.text

    msg = bot.send_message(userID, lang.adminFirst[LANG]["addClubMeetingCount"])
    bot.register_next_step_handler(msg, addClubMeetingCount, bot, LANG, name_club, head_club)


def addClubMeetingCount(message, bot, LANG, name_club, head_club):
    userID = message.chat.id
    # СДЕЛАТЬ ПРОВЕРКУ НА INT
    meeting_count = message.text

    '''Возможно это стоит вынести в отдельную функцию'''
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['confirm'])
    btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
    markup.add(btn1, btn2)

    msg = bot.send_message(userID, lang.adminFirst[LANG]["addClubConfirmation"], reply_markup=markup)
    bot.register_next_step_handler(msg, addClubConfirmation, bot, LANG, name_club, head_club, meeting_count)


def addClubConfirmation(message, bot, LANG, name_club, head_club, meeting_count):
    userID = message.chat.id
    confirmation = message.text

    if confirmation == lang.adminFirst[LANG]['confirm']:
        success = 1
        # здесь должна быть попытка обновить базу данных
        if success:  # если успех, то
            bot.send_message(userID, lang.adminFirst[LANG]["addClubSuccess"])
            '''отправить в call значение, чтобы вернуть админа к списку клубов. почитать как это сделать,
            возможно пусть коля этим занимается'''
        else:  # не успех
            bot.send_message(userID, lang.adminFirst[LANG]['addClubFailed'])
    else:
        bot.send_message(userID, lang.adminFirst[LANG]["addClubCancel"])
    bot.send_message(userID, text=lang.adminFirst[LANG]["all_clubs"],
                     reply_markup=returnAllClubsKeyboard(LANG))

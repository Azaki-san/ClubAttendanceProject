import telebot


import lang
from work_functions import returnAllClubsKeyboard, checkAccountType, getKeyboardleaderOrUser, printingDescription
from adminAddingClub import addNameClub
from work_functions import dbClone
import adminEditingClub

bot = telebot.TeleBot('1786952895:AAHY7ZdGvly2ygQT3EQIFztPyen4c-EcwiY')
# заглушка на случай если будем выпендриваться и добавлять русский перевод бота
LANG = "eng"
ids = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
       '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
       '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50']



@bot.message_handler(content_types=['text'])
def text_handler(message):
    userID = message.chat.id
    # проверка на тип аккаунта, на данный момент администратор единственный
    accountType = checkAccountType(userID, message.from_user.username)
    if accountType == 0:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text=lang.adminFirst[LANG]["all_clubs"],
                                                        callback_data='adminAllClubs'))
        keyboard.add(telebot.types.InlineKeyboardButton(text=lang.adminFirst[LANG]["attendance"],
                                                        callback_data='adminAttendance'))
        bot.send_message(userID, f"{lang.adminFirst[LANG]['hello1']}"
                                          f" {message.from_user.first_name}! {lang.adminFirst[LANG]['hello2']}",
                         reply_markup=keyboard)
    elif accountType == 1:
        bot.send_message(userID, f"{lang.adminFirst[LANG]['hello1']}"
                                 f" {message.from_user.first_name}! {lang.leader[LANG]['choiceText']}",
                         reply_markup=getKeyboardleaderOrUser(userID, LANG))
        """Предоставить выбор как авторизоваться"""
    else:
        """обычный тип, отобразить список всех клубов для регистрации в них"""


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    userID = call.message.chat.id
    messageID = call.message.message_id

    if call.data == "adminAllClubs":
        print(returnAllClubsKeyboard(LANG))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=lang.adminFirst[LANG]["all_clubs"],
                              reply_markup=returnAllClubsKeyboard(LANG))
    elif call.data == "adminAddClub":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = telebot.types.KeyboardButton(lang.adminFirst[LANG]['cancel'])
        markup.add(btn)
        msg = bot.send_message(userID, text=lang.adminFirst[LANG]["addNameClub"], reply_markup = markup)
        bot.register_next_step_handler(msg, addNameClub, bot, LANG)

    elif call.data in ids:
        # загрузка информации о клубе
        # далее создать кнопки
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['editingDescription'])
        btn2 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['deletingClub'])
        btn3 = telebot.types.KeyboardButton(lang.adminFirst[LANG]['back'])
        markup.add(btn1, btn2, btn3)
        clubID = call.data
        msg = bot.send_message(userID, text=printingDescription(LANG, dbClone.return_club_by_id(clubID)[0]),
                               parse_mode='Markdown', reply_markup=markup)
        bot.register_next_step_handler(msg, adminEditingClub.general, bot, LANG, clubID)







bot.polling()





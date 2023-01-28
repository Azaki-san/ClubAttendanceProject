import db
import telebot
import lang

def getAllClubs():
    # вернуть список названий всех клубов в списке
    # формат [['клуб1', '0', ['клуб2', '0']
    # дёрнуть из функции getAllClubsNames и getAllClubsIds
    return [['InnoGameClub', '0'], ['BDSM', '1'], ['InnoSportClub', '2']]


# она реализована, просто находится в этом файле
def returnAllClubsKeyboard(LANG):
    keyboard = telebot.types.InlineKeyboardMarkup()
    allClubs = getAllClubs()
    for i in allClubs:
        keyboard.add(telebot.types.InlineKeyboardButton(text=i[0],
                                                        callback_data=i[1]))
    keyboard.add(telebot.types.InlineKeyboardButton(text=lang.adminFirst[LANG]["add_club"],
                                                    callback_data='adminAddClub'))
    return keyboard

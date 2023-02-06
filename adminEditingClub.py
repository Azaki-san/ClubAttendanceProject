import lang
from working_with_db import WorkingWithDB, dbClone
from work_functions import returnAllClubsKeyboard


def general(message, bot, LANG, clubID):
    msg = message.text
    if msg == lang.adminFirst[LANG]['editingDescription']:
        editingClubInfo(message, bot, LANG, clubID)
    elif msg == lang.adminFirst[LANG]['deletingClub']:
        deletingTheClub(message, bot, LANG, clubID)


def deletingTheClub(message, bot, LANG, clubID):
    userID = message.chat.id
    dbClone.remove_club(clubID)
    bot.send_message(userID, text=f'{lang.adminFirst[LANG]["successfulClubDeleting"]}\n{lang.adminFirst[LANG]["all_clubs"]}',
                     reply_markup=returnAllClubsKeyboard(LANG))


def editingClubInfo(clubID):
    print(clubID)

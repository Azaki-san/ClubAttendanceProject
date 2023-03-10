import working_with_db as db
import telebot
import lang
from working_with_db import dbClone


def getAllClubs(listOfClubs, idOfClubs):
    fullListOfClubs = []
    print(idOfClubs)
    for i in range(len(listOfClubs)):
        fullListOfClubs.append([listOfClubs[i][0], str(eval(idOfClubs[i])[0])])
    print(fullListOfClubs)
    fullListOfClubs.sort(key=lambda x: x[0])
    print(fullListOfClubs)
    return fullListOfClubs


def getKeyboardleaderOrUser(userID, LANG):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, dbClone.get_next_club_id()):
        info = dbClone.return_club_by_id(i)[0]
        leaders = eval(info[2])
        name = info[1]
        if userID in leaders:
            keyboard.add(telebot.types.InlineKeyboardButton(text=name,
                                                            callback_data=f'{i}'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=lang.leader[LANG]["choiceUser"],
                                                    callback_data='userAuth'))
    return keyboard


def printingDescription(LANG, clubInfo):
    name = clubInfo[1]
    idLeader = eval(clubInfo[2])
    amountOfMeetings = clubInfo[3]
    if len(clubInfo) >= 5:
        description = clubInfo[4]
    else:
        description = 'To be added by the Head'
    listOfAliases = []
    for i in range(len(idLeader)):
        alias = dbClone.return_alias_by_tgid(idLeader[i])
        if alias:
            listOfAliases.append(dbClone.return_alias_by_tgid(idLeader[i])[0][0])
    finalString = f"***{lang.adminFirst[LANG]['nameOfTheClub']}***: {name}\n***{lang.adminFirst[LANG]['clubHeads']}***: "
    finalString += getParsedAliases(listOfAliases)
    finalString += f"\n***{lang.adminFirst[LANG]['amountOfMeetings']}***: {amountOfMeetings}\n"
    finalString += f"***{lang.adminFirst[LANG]['clubDescription']}***: {description}"
    return finalString


def getParsedAliases(listOfAliases):
    finalString = ''
    for i in range(len(listOfAliases)):
        k = listOfAliases[i]
        res = ''
        for j in k:
            if j != '_':
                res += j
            else:
                res += '\\'
                res += j
        if i != len(listOfAliases) - 1:
            finalString += f"{res}, "
        else:
            finalString += f"{res}"
    return finalString


# ?????? ??????????????????????, ???????????? ?????????????????? ?? ???????? ??????????
def returnAllClubsKeyboard(LANG):
    keyboard = telebot.types.InlineKeyboardMarkup()
    allClubs = getAllClubs(dbClone.return_all_clubs(), dbClone.return_all_clubids())
    for i in allClubs:
        keyboard.add(telebot.types.InlineKeyboardButton(text=i[0],
                                                        callback_data=i[1]))
    keyboard.add(telebot.types.InlineKeyboardButton(text=lang.adminFirst[LANG]["add_club"],
                                                    callback_data='adminAddClub'))
    return keyboard


def checkAccountType(teleid, alias):
    res = dbClone.is_exist_by_teleid(teleid)
    if res == -1:
        dbClone.register(teleid, "@" + alias.lower())
        fOpened = open("queue.txt", "r+")
        text = fOpened.read()
        dict = eval(text)
        print(type(dict))
        alias = dbClone.return_alias_by_tgid(teleid)
        dbClone.update_type(teleid, str(0))
        if alias[0] in dict:
            for i in dict.get(alias):
                listOldLeaders = eval(dbClone.get_leaders(i)[0])
                listOldLeaders.append(teleid)
                dbClone.update_leaders(str(listOldLeaders), i)
            del dict[alias]
            dbClone.update_type(teleid, str(1))
            fOpened.seek(0)
            fOpened.write(str(dict))
    """???? ???????? ?????????????? ????????????????????????????, ?????? ?????????????????????? ??????????????????, ?????????? ???????????????? ???? ?????? ????????????????."""
    nowType = dbClone.return_type(teleid)[0][0]
    return nowType


print(dbClone.return_club_by_id(0))
a = printingDescription('eng', (0, 'InnoGameClub', '[592651306, 981241]', 2, '??????????', None))
print(a)

import db
import telebot
import lang
dbClone = db.WorkingWithDB()
def getAllClubs(LANG, listOfClubs, idOfClubs):
    fullListOfClubs = []
    for i in range(len(listOfClubs)):
        fullListOfClubs.append([listOfClubs[i], idOfClubs[i]])
    return fullListOfClubs

def printingDescription(clubInfo):
    name = clubInfo[1]
    idLeader = eval(clubInfo[2])
    amountOfMeetings = clubInfo[3]
    description = clubInfo[4]
    listOfAliases = []
    for i in range(len(idLeader)):
        listOfAliases.extend(dbClone.return_alias_by_tgid(idLeader[i]))
    finalString = f"**{lang.adminFirst[LANG]['nameOfTheClub']}**: {name}\n**{lang.adminFirst[LANG]['clubHeads']}**: "
    for i in range(len(listOfAliases)):
        if i != len(listOfAliases) - 1:
            finalString += f"{listOfAliases[i]}, "
        else:
            finalString += f"{listOfAliases[i]}"
    finalString += f"**{lang.adminFirst[LANG]['amountOfMeetings']}**: {amountOfMeetings}"
    finalString += f"**{lang.adminFirst[LANG]['clubDescription']}**: {description}"
    return finalString


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

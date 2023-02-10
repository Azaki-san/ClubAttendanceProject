import sqlite3

class WorkingWithDB:

    def __init__(self):
        self.cursor, self.connection = self.connect_to_database()

    def connect_to_database(self):
        connection = sqlite3.connect("TelebotDB.db", check_same_thread=False)
        cursor = connection.cursor()
        return cursor, connection

    def return_type(self, telegram_id):
        self.cursor.execute("SELECT Type FROM people WHERE TelegramID = " + str(telegram_id) + ";")
        res = self.cursor.fetchall()
        return res

    def return_all_clubs(self):
        self.cursor.execute("SELECT Name FROM clubs ORDER by ID;")
        res = self.cursor.fetchall()
        return res

    def return_all_clubids(self):
        self.cursor.execute("SELECT ID FROM clubs;")
        res = self.cursor.fetchall()
        for i in range(len(res)):
            res[i] = str(res[i])
        return res

    def create_new_club(self, ame, amount_of_meetings, leaders):
        temp = ('INSERT INTO clubs (ID, Name, LeaderID, AmountOFMeetings) VALUES (' + str(
            self.get_next_club_id()) + ', "' + ame + '", "' + str(leaders)
                + '", ' + str(amount_of_meetings) + ');')
        print(temp)
        self.cursor.execute(temp)
        self.connection.commit()
        return 1

    def add_a_description(self, description, id):
        self.cursor.execute("UPDATE clubs SET Description = '" + description + "' WHERE ID = " + str(id) + ";")
        self.connection.commit()

    def return_club_by_id(self, id):
        self.cursor.execute("SELECT * FROM clubs WHERE ID = " + str(id) + ";")
        res = self.cursor.fetchall()
        return res

    def change_name_of_club(self, new_name, id):
        self.cursor.execute("UPDATE clubs SET Name = '" + new_name + "' WHERE ID = " + str(id) + ";")
        self.connection.commit()

    def change_amount_of_meetings(self, new_amount, id):
        self.cursor.execute("UPDATE clubs SET AmountOfMeetings = " + new_amount + " WHERE ID = " + str(id) + ";")
        self.connection.commit()

    def return_alias_by_tgid(self, tgid):
        self.cursor.execute("SELECT Alias FROM people WHERE TelegramID = '" + str(tgid) + "';")
        res = self.cursor.fetchall()
        return res

    def add_a_picture(self, clubid, pict):
        self.cursor.execute("UPDATE clubs SET Picture = " + pict + " WHERE ID = " + str(clubid) + ";")
        self.connection.commit()

    def register(self, teleid, alias):
        self.cursor.execute("INSERT INTO people(ID, TelegramID, Alias, Type) VALUES(" + str(self.get_next_people_id())
                            + ", " + str(teleid) + ", '" + str(alias) + "', 2);")
        self.connection.commit()

    def is_exist(self, alias):
        self.cursor.execute('SELECT TelegramID FROM people WHERE Alias = ?', (alias,))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return -1
        else:
            return str(res[0])

    def is_exist_by_teleid(self, teleid):
        self.cursor.execute('SELECT TelegramID FROM people WHERE TelegramID = ?', (teleid,))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return -1
        else:
            return str(res[0])

    def update_type(self, teleid, type):
        self.cursor.execute("UPDATE people SET Type = " + str(type) + " WHERE TelegramID = " + str(teleid) + ";")
        self.connection.commit()

    def get_next_club_id(self):
        res = self.cursor.execute("SELECT MAX(ID) FROM clubs;").fetchone()
        if res[0] is None:
            return 1
        else:
            return res[0] + 1

    def get_next_people_id(self):
        res = self.cursor.execute("SELECT MAX(ID) FROM people;").fetchone()
        return res[0] + 1

    def update_leaders(self, st, clubid):
        self.cursor.execute('UPDATE clubs SET LeaderID = "' + str(st) + '" WHERE ID = ' + str(clubid) + ';')

    def get_leaders(self, clubid):
        res = self.cursor.execute("SELECT LeaderID FROM clubs WHERE ID = " + str(clubid) + ";").fetchone()
        return res

    def remove_club(self, clubid):
        self.cursor.execute("DELETE FROM clubs WHERE ID = '" + clubid + "';")
        self.connection.commit()

    def add_type(self, id, type):
        self.cursor.execute("UPDATE clubs SET Type = " + str(type) + " WHERE ID = " + str(id) + ";")

dbClone = WorkingWithDB()


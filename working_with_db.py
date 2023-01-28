import sqlite3


class WorkingWithDB:

    def __init__(self):
        self.cursor, self.connection = self.connect_to_database()
        self.next_club_id = 1
        self.next_people_id = 1

    def connect_to_database(self):
        connection = sqlite3.connect("TelebotDB.db")
        cursor = connection.cursor()
        return cursor, connection

    def return_type(self, telegram_id):
        self.cursor.execute("SELECT Type FROM people WHERE TelegramID = " + str(telegram_id) + ";")
        res = self.cursor.fetchall()
        return res

    def return_all_clubs(self):
        self.cursor.execute("SELECT Name FROM clubs;")
        res = self.cursor.fetchall()
        return res

    def return_all_clubids(self):
        self.cursor.execute("SELECT ID FROM clubs;")
        res = self.cursor.fetchall()
        for i in range(len(res)):
            res[i] = str(res[i])
        return res

    def create_new_club(self, name, amount_of_meetings, leaders):
        self.cursor.execute("INSERT INTO clubs VALUES(" + str(self.next_club_id) + ", " + name + ", " + str(leaders)
                            + ", " + str(amount_of_meetings) + ", " + "NULL);")
        self.connection.commit()
        self.next_club_id += 1

    def add_a_description(self, description, id):
        self.cursor.execute("UPDATE clubs SET Description = " + description + " WHERE ID = " + str(id) + ";")
        self.connection.commit()

    def return_club_by_id(self, id):
        self.cursor.execute("SELECT * FROM clubs WHERE ID = " + str(id) + ";")
        res = self.cursor.fetchall()
        return res

    def change_name_of_club(self, new_name, id):
        self.cursor.execute("UPDATE clubs SET Name = " + new_name + " WHERE ID = " + str(id) + ";")
        self.connection.commit()

    def change_amount_of_meetings(self, new_amount, id):
        self.cursor.execute("UPDATE clubs SET AmountOfMeetings = " + new_amount + " WHERE ID = " + str(id) + ";")
        self.connection.commit()






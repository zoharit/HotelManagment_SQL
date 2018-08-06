import sqlite3
import time


class hotelWorker():

    def __init__(self):
        pass

    def dohoteltask(self, taskname, parameter):

        conn = sqlite3.connect('cronhoteldb.db')

        if 'clean' in taskname:
            cleaning_lady = "Rooms "
            cursor = conn.execute("SELECT RoomNumber from Rooms")
            rooms = []
            for row in cursor:
                cursor2 = conn.execute("SELECT RoomNumber FROM Residents WHERE RoomNumber = ?", row)
                data = cursor2.fetchone()
                if data is None:
                    rooms.append(str(row[0]))
            rooms.sort()
            for x in rooms:
                cleaning_lady += x + ", "
                
            cleaning_lady = cleaning_lady[:-2]
            t = time.time()
            cleaning_lady += " were cleaned at " + str(t)
            print cleaning_lady
            return t

        elif 'breakfast' in taskname:
            params = (parameter,)
            cursor = conn.execute("SELECT FirstName,LastName from Residents WHERE  RoomNumber = ?", params)
            data = cursor.fetchone()
            t = time.time()
            print str(data[0]) + " " + str(data[1]) + " in room " + str(parameter) + \
                  " has been served breakfast at " + str(time.time())
            return t

        else:
            params = (parameter,)
            cursor = conn.execute("SELECT FirstName,LastName from Residents WHERE  RoomNumber = ?", params)
            data = cursor.fetchone()
            t = time.time()
            print str(data[0]) + " " + str(data[1]) + " in room " + str(parameter) + \
                  " received a wakeup call at " + str(time.time())
            return t
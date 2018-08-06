import sqlite3
import sys
import os.path

def createdatabase():
    conn = sqlite3.connect('cronhoteldb.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS TaskTimes
       (TaskId INT PRIMARY KEY     NOT NULL,
       DoEvery        INT    NOT NULL,
       NumTimes       INT     NOT NULL);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS Tasks
       (TaskId INT NOT NULL REFERENCES TaskTimes(TaskId),
       TaskName        TEXT    NOT NULL,
       Parameter       INT     NOT NULL);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS Rooms
       (RoomNumber INT PRIMARY KEY
        );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS Residents
       (RoomNumber INT NOT NULL REFERENCES Rooms(RoomNumber),
       FirstName      TEXT    NOT NULL,
       LastName       TEXT     NOT NULL);''')

    conn.close()


def configureDB(config):
    conn = sqlite3.connect('cronhoteldb.db')
    taskid = 0
    with open(config) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    for line in content:
        check = line.split(",")[0]
        if 'room' in check:
            params = (line.split(",")[1],)
            conn.execute("INSERT INTO Rooms VALUES (?)", params)
            if len(line.split(',')) is 4:
                params = (line.split(",")[1], line.split(",")[2], line.split(",")[3])
                conn.execute("INSERT INTO Residents VALUES (?,?,?)", params)
        elif 'clean' in check:
            params = (taskid, line.split(",")[1], line.split(",")[2])
            conn.execute("INSERT INTO TaskTimes VALUES (?,?,?)", params)
            params = (taskid, line.split(",")[0], 0)
            conn.execute("INSERT INTO Tasks VALUES (?,?,?)", params)
            taskid += 1
        else:
            params = (taskid, line.split(",")[1], line.split(",")[3])
            conn.execute("INSERT INTO TaskTimes VALUES (?,?,?)", params)
            params = (taskid, line.split(",")[0], line.split(",")[2])
            conn.execute("INSERT INTO Tasks VALUES (?,?,?)", params)
            taskid += 1

    conn.commit()
    conn.close()

def printDB():
    conn = sqlite3.connect('cronhoteldb.db')
    cursor = conn.execute("SELECT RoomNumber, FirstName, LastName  from Residents")
    for row in cursor:
        print "RoomNumber = ", row[0]
        print "FirstName = ", row[1]
        print "LastName = ", row[2], "\n"

    print "Operation done successfully";

    cursor = conn.execute("SELECT TaskId, DoEvery, NumTimes  from TaskTimes")
    for row in cursor:
        print "TaskId = ", row[0]
        print "DoEvery = ", row[1]
        print "NumTimes = ", row[2], "\n"

    print "Operation done successfully";

    cursor = conn.execute("SELECT TaskId, TaskName, Parameter  from Tasks")
    for row in cursor:
        print "TaskId = ", row[0]
        print "TaskName = ", row[1]
        print "Parameter = ", row[2], "\n"

    print "Operation done successfully";

    cursor = conn.execute("SELECT RoomNumber  from Rooms")
    for row in cursor:
        print "RoomNumber = ", row[0], "\n"

    print "Operation done successfully";

    conn.commit()
    conn.close()


def main(config):
    if not os.path.exists('cronhoteldb.db') and config is not None:
        createdatabase()
        configureDB(config)

if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1])
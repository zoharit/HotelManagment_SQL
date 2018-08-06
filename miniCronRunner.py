import sqlite3
import shutil
import hotelWorker
import os
import time


class miniCronRunner:
    def __init__(self):
        self.tasks = {}
        pass

    def Read(self):
        conn = sqlite3.connect('cronhoteldb.db')
        cursor = conn.execute(
            "SELECT Tasks.TaskId, TaskName ,Parameter, DoEvery from TaskTimes,"
            " Tasks WHERE TaskTimes.TaskId = Tasks.TaskId and NumTimes > 0")
        rows = cursor.fetchall()
        for row in rows:
            self.taskRunner(row[0], row[1], row[2], row[3])

        cond = conn.execute("SELECT TaskId from TaskTimes where NumTimes > 0")
        to_do = cond.fetchall()
        while to_do is not None and len(to_do) > 0 and os.path.exists('cronhoteldb.db'):
            for do in to_do:
                cursor = conn.execute(
                        "SELECT Tasks.TaskId, TaskName ,Parameter, DoEvery from TaskTimes,"
                        " Tasks WHERE TaskTimes.TaskId = Tasks.TaskId and Tasks.TaskId = ?", do)
                data = cursor.fetchone()
                if do[0] in self.tasks and self.tasks[do[0]] <= time.time():
					del self.tasks[do[0]]
					self.taskRunner(data[0], data[1], data[2], data[3])
                cursor.close()
            cond = conn.execute("SELECT TaskId from TaskTimes where NumTimes > 0")
            to_do = cond.fetchall()
        cond.close()

        conn.commit()
        conn.close()

    def Update(self, id):
        conn = sqlite3.connect('cronhoteldb.db')
        params = (id,)
        val = conn.execute("SELECT NumTimes from TaskTimes where TaskId=?", params)
        data = val.fetchone()
        arg = data[0] - 1
        params = (arg, id)
        conn.execute("UPDATE TaskTimes set NumTimes = ? where TaskId=?", params)
        conn.commit()
        conn.close()
        return arg

    def taskRunner(self, id, TaskName, Parameter, DoEvery):

        Worker = hotelWorker.hotelWorker()
        t = Worker.dohoteltask(TaskName, Parameter)
        num = self.Update(id)
        if num > 0:
            self.tasks[id] = t + float(DoEvery)


def main():
    if os.path.exists('cronhoteldb.db'):
        runner = miniCronRunner()
        runner.Read()


if __name__ == "__main__":
    main()
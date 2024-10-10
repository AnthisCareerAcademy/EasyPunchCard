from datetime import datetime
import sqlite3

class Clock:
    """
    Clock class will allow User to punch in or punch out and record the time spent between
    Execute the close method after done using Clock class
    """
    def __init__(self, unique_id: str, database_path: str) -> None:
        self.id = unique_id
        self.conn = sqlite3.connect(database_path)
        self.working = self.conn.execute(f"SELECT working FROM students WHERE id = {self.id}")

    def punch_in(self):
        if self.working:
            return
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE students SET working = 1 WHERE id = {self.id}")
        cursor.execute(f"UPDATE students SET start_time = '{datetime.now()}' WHERE id = {self.id}")
        self.conn.commit()
        cursor.close()

    def punch_out(self):
        if not self.working:
            return
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE students SET working = 0 WHERE id = {self.id}")
        end_time = datetime.now()
        cursor.execute(f"UPDATE students SET start_time = '{end_time}' WHERE id = {self.id}")
        cursor.execute(f"SELECT start_time FROM students WHERE id = {self.id}")
        start_time = datetime.strptime((cursor.fetchone())[0], "%Y-%m-%d %H:%M:%S.%f")
        total_minutes_worked = ((end_time-start_time).total_seconds())/60
        cursor.execute(f"SELECT total_minutes FROM students WHERE id = {self.id}")
        total_minutes = (cursor.fetchone())[0] + format(total_minutes_worked, '.2f')
        cursor.execute(f"UPDATE students SET total_hours = {total_minutes} WHERE id = {self.id}")
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()
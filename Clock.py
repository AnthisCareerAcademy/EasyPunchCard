from datetime import datetime
from database import SqlAccess

class Clock:
    """
    Clock class will allow User to clock in or clock out and record the time spent between
    Execute the close method after done using Clock class
    """
    def __init__(self, student_id: str) -> None:
        self.id = student_id
        # by now the student should be in the database
        self.access = SqlAccess(student_id)

    def clock_in(self):
        conn = self.access.get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT total_minutes FROM all_users WHERE student_id = %s", (self.id,))
        total_minutes = cursor.fetchone()[0]
        date = datetime.now().strftime("%m/%d/%Y")
        start_time = datetime.now()
        query = f"""INSERT INTO user_{self.id} (student_id, date, start_time, end_time, total_minutes) 
                VALUES (%s, %s, %s, NULL, %s)"""
        values = (self.id, date, start_time, total_minutes)  # Ensure total_minutes is defined
        # values will be updated again once user clocks out
        cursor.execute(query, values)
        cursor.execute("UPDATE all_users SET start_time = %s WHERE student_id = %s", (start_time, self.id))
        conn.commit()

        cursor.close()
        conn.close()
    
    def clock_out(self):
        conn = self.access.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT start_time FROM all_users WHERE student_id = %s", self.id)
        # turn back into datetime object
        start_time = datetime.strptime((cursor.fetchone())[0], "%Y-%m-%d %H:%M:%S.%f")
        cursor.execute("SELECT total_minutes FROM all_users WHERE student_id = %s", self.id)
        total_minutes = int(cursor.fetchone()[0])
        end_time = datetime.now()
        time_worked = int((end_time-start_time).total_seconds()/60)
        total_minutes += time_worked
        # reset start time and update total minutes in all_users
        cursor.execute("UPDATE all_users SET total_minutes = %s, start_time = NULL WHERE student_id = %s", (total_minutes, self.id))
        # update end time and total_minutes in user table
        cursor.execute(f"UPDATE user_{self.id} end_time = %s, total_minutes = %s WHERE student_id = %s", (end_time, total_minutes, self.id))
        conn.commit()

        cursor.close()
        conn.close()
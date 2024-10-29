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
        #TODO: make it so you can't clock in if you're already clocked in
        conn = self.access.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT working_status FROM all_users WHERE student_id = ?", (self.id,))
        working = cursor.fetchone()[0]
        if working == 1:
            cursor.close()
            conn.close()
            print("User is already clocked in!")
            return

        cursor.execute("SELECT total_minutes FROM all_users WHERE student_id = ?", (self.id,))
        total_minutes = cursor.fetchone()[0]
        date = datetime.now().strftime("%m/%d/%Y")
        start_time = datetime.now()
        query = f"""INSERT INTO user_{self.id} (student_id, date, start_time, end_time, total_minutes) 
                VALUES (?, ?, ?, NULL, ?)"""
        values = (self.id, date, start_time, total_minutes)
        # values will be updated again once user clocks out
        cursor.execute(query, values)
        cursor.execute("UPDATE all_users SET start_time = ?, working_status = 1 WHERE student_id = ?", (start_time, self.id))
        conn.commit()

        cursor.close()
        conn.close()
    

    def clock_out(self):
        conn = self.access.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT start_time FROM all_users WHERE student_id = ?", (self.id,))
        start_time = cursor.fetchone()[0]

        # if no start time, the user is already clocked out
        if start_time == None:
            cursor.close()
            conn.close()
            print("User is already clocked out!")
            return
        
        # turn back into datetime object
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        cursor.execute("SELECT total_minutes FROM all_users WHERE student_id = ?", (self.id,))
        total_minutes = int(cursor.fetchone()[0])
        end_time = datetime.now()
        time_worked = int((end_time-start_time).total_seconds()/60)
        total_minutes += time_worked

        # update end time and total_minutes in user table
        cursor.execute(f"UPDATE user_{self.id} SET end_time = ?, total_minutes = ? WHERE start_time = ?", (end_time, total_minutes, start_time))
        # reset start time and update total minutes in all_users
        cursor.execute("UPDATE all_users SET total_minutes = ?, start_time = NULL, working_status = 0 WHERE student_id = ?", (total_minutes, self.id))
        conn.commit()

        cursor.close()
        conn.close()
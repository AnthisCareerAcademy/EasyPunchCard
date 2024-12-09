from datetime import datetime
from database import SqlAccess

class Clock:
    """
    Clock class will allow User to clock in or clock out and record the time spent between
    Execute the close method after done using Clock class

    Attributes:
        id (str): The unique identifier (student_id) for the user.
        access (SqlAccess): An instance of the SqlAccess class that manages the user's data and database access.

    Args:
        student_id (str): The ID of the student using the clocking system.
    """
    def __init__(self, student_id: str) -> None:
        """
        Initializes the clock class for a specific user

        Args:
            student_id (str): The ID of the student clocking in/out.
        
        Initializes the `access` attribute, which provides access to the user's database records.
        """
        self.id = student_id
        self.access = SqlAccess(student_id)


    def clock_in(self):
        """
        Clocks the user in if they aren't already clocked in

        - Checks if the user is already clocked in (working_status = 1).
        - Inserts a record in the user's specific table (`user_{student_id}`) with the clock-in time.
        - Updates the user's `working_status` to 1 and stores the start time in the `all_users` table.

        Raises:
            sqlite3.OperationalError: If there is an issue with the database query execution.
        """
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
        """
        Clocks the user out if they aren't already clocked out
        
        - Checks if the user has a start time recorded. If not, the user is already clocked out.
        - Calculates the time worked and updates the user's table with the end time and total minutes worked.
        - Resets the start time and updates the `working_status` and `total_minutes` in the `all_users` table.

        Raises:
            sqlite3.OperationalError: If there is an issue with the database query execution.
        """
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
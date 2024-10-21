import sqlite3

class SqlAccess:
    """alskdfjlkasjf"""
    def __init__(self, student_id:str, admin_status:int=None):
        self.create_table()
        self.student_id = student_id
        self.exists = self.user_exists()
        if self.exists:
            # check if user exists
            conn = self.get_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT admin_status FROM all_users WHERE student_id='{self.student_id}'")
            self.admin_status = cursor.fetchone()[0]
            cursor.close()
            conn.close()
        else:
            if admin_status in [0, 1]:
                self.admin_status = admin_status
            else:
                raise ValueError("User does not exist and no correct data provided for admin_status")
        
        

    @staticmethod
    def get_db():
        conn = sqlite3.connect('EasyPunchCard.db')
        return conn
    
    def user_exists(self):
        # is the user is the all_users table
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id='{self.student_id}')")
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists


    def create_table(self):
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS all_users(
                       student_id TEXT PRIMARY KEY,
                       username TEXT NOT NULL,
                       admin_status INT NOT NULL,
                       total_minutes INT
                       )
                       ''')
        conn.commit()
        cursor.close()
        conn.close()


    def add_self(self, username:str):
        conn = self.get_db()
        cursor = conn.cursor()
        # Add user into main table
        cursor.execute(f'''
                        INSERT INTO all_users(student_id, username, admin_status, total_minutes)
                        VALUES('{self.student_id}', '{username}', {self.admin_status}, 0)
                        ''')
        # create table for user
        cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS user_{self.student_id} (
                        student_id TEXT,
                        date TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        total_minutes INT,
                        CONSTRAINT FK_student_id FOREIGN KEY (student_id)
                        REFERENCES all_users(student_id)
                        )
                        ''')
        conn.commit()
        cursor.close()
        conn.close()


    def update_time(self, additional_minutes:int):
        """
        conn = self.get_db()
        get cursor
        total_minutes = total_minutes from all_students of student_id
        total_minutes += additional_minutes

        ***from Clock class (after clocking in and clocking out) get date, start_time, and end_time
        ***issue here

        query to insert a row into user table
        'INSERT INTO user_{student_id}(student_id, date, start_time, end_time, total_minutes)
        VALUES({student_id}, {date}, {start_time}, {end_time}, {total_minutes})'
        update total_minutes in all_users
        'UPDATE all_users SET total_minutes = {total_minutes} WHERE student_id = {student_id}'

        commit the queries
        close the cursor
        close the connection
        """

    def read_all_users(self):
        if self.admin_status == 0:
            return "user doesn't have admin status"
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM all_users""")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    
    def read_user_table(self, student_id):
        if self.admin_status == 0:
            return "user doesn't have admin status"
        conn = self.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""SELECT * FROM user_{student_id}""")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except sqlite3.OperationalError as e:
            cursor.close()
            conn.close()
            return f"{e}"

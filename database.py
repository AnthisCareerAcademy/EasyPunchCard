import sqlite3

class SqlAccess:
    """alskdfjlkasjf"""
    def __init__(self):
        pass

    @staticmethod
    def get_db():
        conn = sqlite3.connect('EasyPunchCard.db')
        return conn

    def create_table(self):
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS all_users (
                       student_id TEXT PRIMARY KEY,
                       username TEXT NOT NULL,
                       admin_status INT NOT NULL,
                       total_minutes INT
                       )
                       ''')
        conn.commit()
        cursor.close()
        conn.close()


    def add_user(self, student_id:str, username:str, admin_status:int):
        conn = self.get_db()
        cursor = conn.cursor()
        # Add user into main table
        cursor.execute(f'''
                        INSERT INTO all_users(student_id, username, admin_status, total_minutes)
                        VALUES('{student_id}', '{username}', {admin_status}, 0)
                        ''')
        # create table for user
        cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS user_{student_id} (
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


    def update_time(self, student_id:str, additional_minutes:int):
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
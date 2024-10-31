import sqlite3
from pandas import read_sql_query

class SqlAccess:
    """Allows the User Class to connect to the EasyPunchCard database. Creates table, allows all users to add themself, and allows admins reads data."""
    def __init__(self, student_id:str, admin_status:int=None):
        self.create_table()
        self.student_id = student_id
        self.exists = self.user_exists()
        if self.exists:
            # check if user exists
            conn = self.get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT admin_status FROM all_users WHERE student_id = ?", (self.student_id,))
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
        cursor.execute("SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id = ?)", (self.student_id,))
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
                       start_time TEXT,
                       working_status INT,
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
        cursor.execute('''
                       INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes)
                       VALUES (?, ?, ?, NULL, 0, 0)
                       ''', (self.student_id, username, self.admin_status))
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

    def add_user(self, student_id:str, username:str, admin_status:int):
        if self.admin_status == 0:
            raise "Error: user doesn't have admin status"
        
        with self.get_db() as conn:
            cursor = conn.cursor()

            # user is not an admin
            if admin_status == 0:
                cursor.execute('''
                INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes)
                VALUES (?, ?, ?, NULL, 0, 0)
                ''', (student_id, username, admin_status))

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

            # user is an admin
            elif admin_status == 1:
                cursor.execute('''
                INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes)
                VALUES (?, ?, ?, NULL, 0, 0)
                ''', (student_id, username, admin_status))
                conn.commit()
                cursor.close()

                  
    def remove_user(self, student_id:str):
        if self.admin_status == 0:
            raise "Error: user doesn't have admin status"
        if self.student_id == student_id:
            raise "Error: can't delete self"
        with self.get_db() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM "
        # will finish later

        
                


        


    def update_time(self, additional_minutes:int):
        """
        conn = self.get_db()
        get cursor
        total_minutes = total_minutes from all_students of student_id
        total_minutes += additional_minutes

        ***from Clock class (after clocking in and clocking out) get date, start_time, and end_time
        ***issue here

        query to insert a row into user table
        'INSERT INTO user_{student_id}INSERT INTO user_{student_id}(student_id, date, start_time, end_time, total_minutes)
        VALUES({student_id}, {date}, {start_time}, {end_time}, {total_minutes})'
        update total_minutes in all_users
        'UPDATE all_users SET total_minutes = {total_minutes} WHERE student_id = {student_id}'

        commit the queries
        close the cursor
        close the connection
        """


    def read_all_users(self):
        if self.admin_status == 0:
            raise "Error: user doesn't have admin status"
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM all_users""")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    

    def read_user_table(self, student_id):
        if self.admin_status == 0:
            raise "Error: user doesn't have admin status"
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
        
    def read_self_table(self):
        conn = self.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""SELECT * FROM user_{self.student_id}""")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except sqlite3.OperationalError as e:
            cursor.close()
            conn.close()
            return f"{e}"
        
    def get_column_from_all_user(self, column_name:str):
        with self.get_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT {column_name} FROM all_user WHERE student_id = ?"
            cursor.execute(query, (self.student_id,))
            # data from that column
            data = cursor.fetchone()[0]
            cursor.close()
            conn.close()
        return data
          
    def database_to_excel(self, sql_table_name:str, file_name:str="EasyPunchCard"):
        """
        Export the records from the database to an Excel file.
        arguments are SQLite table name and the name you want the file to be (default is 'EasyPunchCard')
        """
        if self.admin_status == 0:
            raise "Error: user doesn't have admin status"
        
        query = f'SELECT * FROM {sql_table_name}'
        conn = self.get_db()
        df = read_sql_query(query, conn)
        df.to_excel(f"{file_name}.xlsx", index=True)
        conn.close()

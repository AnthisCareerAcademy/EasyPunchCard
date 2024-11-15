import sqlite3
from pandas import read_sql_query

class SqlAccess:
    """
    Allows the User Class to connect to the EasyPunchCard database. 
    """
    def __init__(self, student_id:str):
        self.create_table()
        self.student_id = student_id
        self.exists = self.user_exists()
        if self.exists:
            # check if user exists
            with self.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT admin_status FROM all_users WHERE student_id = ?", (self.student_id,))
                self.admin_status = cursor.fetchone()[0]
        else:
            # if the user doesn't exist, raise an error
            raise ValueError("User does not exist")
        

    @staticmethod
    def get_db():
        conn = sqlite3.connect('EasyPunchCard.db')
        return conn
    

    def user_exists(self):
        """
        check if the student_id is in the all_users table
        """
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id = ?)", (self.student_id,))
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists


    def create_table(self):
        with self.get_db() as conn:
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
            
            # Check if the admin user already exists
            cursor.execute("SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id = '0000')")
            exists = cursor.fetchone()[0]
            
            # Insert the admin user only if they do not exist
            if not exists:
                cursor.execute('''
                    INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('0000', 'admin_user', 1, None, 0, 0))
            
            conn.commit()

    def add_self(self, username:str):
        """
        allows any user to add themselves to the database
        """
        conn = self.get_db()
        cursor = conn.cursor()
        if self.user_exists():
            raise ValueError("ERROR: user already exists")
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
        """
        allows admin users to add users to the database
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
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
        """
        allows admin users to remove users from the database
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        if self.student_id == student_id:
            raise TypeError("Error: can't delete self")
        with self.get_db() as conn:
            cursor = conn.cursor()
            admin_status = self.admin_get_data_all_users(student_id, "admin_status")
            if admin_status == 1:
                query = "DELETE FROM all_users WHERE student_id = ?"
                cursor.execute(query, (student_id,))
                conn.commit()
                cursor.close()
            else:
                query = "DELETE FROM all_users WHERE student_id = ?"
                cursor.execute(query, (student_id,))
                cursor.execute(f"DROP TABLE user_{student_id}")
                conn.commit()
                cursor.close()


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


    def admin_read_all_users(self):
        """
        allows admin to retrieve all the data form the all_users table
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM all_users""")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    

    def admin_read_self_table(self, student_id:str):
        """
        allow admin users to retreive all the data from a specified user_(ID) table
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
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
        """
        allows the user to retreive all the data from their own user_(ID) table
        """
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
        

    def get_data_all_users(self, column_name:str):
        """
        allow user to read a single cell from their own row on all_users
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT {column_name} FROM all_users WHERE student_id = ?"
            cursor.execute(query, (self.student_id,))
            # data from that column
            data = cursor.fetchone()[0]
        return data
    
    
    def admin_get_data_all_users(self, student_id:str, column_name:str):
        """
        Allows admins to read a single cell from all_users of a specified ID and column name
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        with self.get_db() as conn:
            cursor = conn.cursor()
            query = f"SELECT {column_name} FROM all_users WHERE student_id = ?"
            cursor.execute(query, (student_id,))
            # data from that column
            data = cursor.fetchone()[0]
        return data
    

    def admin_get_row_all_users(self, student_id:str):
        """
        allows admin to retrieve a specified user's row from all_users table
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        try:
            with self.get_db() as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM all_users WHERE student_id = ?"
                cursor.execute(query, (student_id,))
                # Fetch one row from the result
                data = cursor.fetchone()
                if data is None:
                    return None
                return data
        except Exception as e:
            # Log the error, or raise a custom exception if needed
            raise RuntimeError(f"Error retrieving data: {str(e)}")
          

    def database_to_excel(self, sql_table_name:str, file_name:str="EasyPunchCard"):
        """
        Export the records from the database to an Excel file.
        arguments are SQLite table name and the name you want the file to be (default is 'EasyPunchCard')
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        query = f'SELECT * FROM {sql_table_name}'
        conn = self.get_db()
        df = read_sql_query(query, conn)
        df.to_excel(f"{file_name}.xlsx", index=True)
        conn.close()

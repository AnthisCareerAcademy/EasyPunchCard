import sqlite3
from pandas import read_sql_query

class SqlAccess:
    """
    Allows the User Class to connect to the EasyPunchCard database. 
    """
    def __init__(self, student_id:str):
        """
        Initializes SqlAccess for the user

        Args:
            student_id (str): The student id of the user
        """
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
        """
        Creates a connection to the database.

        Returns:
            sqlite3.Connection: A connection object for the SQLite database.
        """
        conn = sqlite3.connect('EasyPunchCard.db')
        return conn
    

    def user_exists(self):
        """
        Checks if the user exists in the database using their student id.

        Returns:
            int: 1 if the user exists, 0 otherwise.
        """
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id = ?)", (self.student_id,))
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists


    def create_table(self):
        """
        Sets up the database table with an admin user if they do not already exist:
        - `all_users`: Stores student ids, username, admin status, start time, working status, total minutes, and graduation year.
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS all_users(
                    student_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    admin_status INT NOT NULL,
                    start_time TEXT,
                    working_status INT,
                    total_minutes INT,
                    graduation_year INT
                )
            ''')
            
            # Check if the admin user already exists
            cursor.execute("SELECT EXISTS(SELECT 1 FROM all_users WHERE student_id = '0000')")
            exists = cursor.fetchone()[0]
            
            # Insert the admin user only if they do not exist
            if not exists:
                cursor.execute('''
                    INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes, graduation_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', ('0000', 'admin_user', 1, None, 0, 0, None))
            
            conn.commit()

    def add_user(self, student_id:str, username:str, admin_status:int, graduation_year: int):
        """
        Allows admin users to add users to the database

        Args:
            student_id (str): The student id of the user being added (can't used already)
            username (str): The username of the user being added to the database
            admin_status (int): The admin status of the user being added (only 1 or 0)
            graduation_year (int): The graduation year of the user being added

        Raises:
            ValueError: If the user trying to add another user doesn't have admin status
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        with self.get_db() as conn:
            cursor = conn.cursor()

            # user is not an admin
            if admin_status == 0:
                cursor.execute('''
                INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes, graduation_year)
                VALUES (?, ?, ?, NULL, 0, 0, ?)
                ''', (student_id, username, admin_status, graduation_year))

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
                INSERT INTO all_users (student_id, username, admin_status, start_time, working_status, total_minutes, graduation_year)
                VALUES (?, ?, ?, NULL, 0, 0, 0000)
                ''', (student_id, username, admin_status))
                conn.commit()
                cursor.close()

                  
    def remove_user(self, student_id:str):
        """
        Allows admin users to remove users from the database

        Args:
            student_id (str): the student id of the user the admin want to remove

        Raises:
            ValueError: If user doesn't have admin status
            TypeError: If the admin user is attempting to remove itself
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
        Allows admins to add additional time to a specific user's total minutes
        """


    def admin_read_all_users(self):
        """
        allows admins to retrieve all the data form the all_users table

        Returns:
            list: A list (called data) of all the users in the "all_users" table

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
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
        Allow admin users to retrieve all the data from a specified user_(ID) table

        Args:
            student_id (str): The student id of the user whose data is being retrieved 

        Returns:
            list: A list (called data) of everything in the specified user's table

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
            sqlite3.OperationalError: If the query failed
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
        Allows the user to retrieve all the data from their own user_(ID) table

        Raises:
            sqlite3.OperationalError: If the query failed
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
        allow user to read a single cell from their row on all_users

        Args:
            column_name (str): The column name from the "all_users" table that the data is being retrieved from

        Returns:
            return_type_varies: Returns the data that is retrieved from the specific column on their row on the "all_users" table
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

        Args:
            column_name (str): The column name from the "all_users" table that the data is being retrieved from
            student_id (str): The student id is the row on the "all_users" table where data is being retrieved from

        Returns:
            return_type_varies: Returns the data that is retrieved from the specified column on row on the "all_users" table

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
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

        Args:
            student_id (str): the student id of the user whose row is being retrieved from "all_users"

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
            RuntimeError: If there's an error while retrieving data
        
        Returns:
            tuple: if a row is returned from the database a tuple containing the user's row will be returned
            None: if no row matches the query
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

        Args:
            sql_table_name (str): SQLite table name
            file_name (str) default = "EasyPunchCard": the name of the file (default is 'EasyPunchCard')

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        query = f'SELECT * FROM {sql_table_name}'
        conn = self.get_db()
        df = read_sql_query(query, conn)
        df.to_excel(f"{file_name}.xlsx", index=True)
        conn.close()

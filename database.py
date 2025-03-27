import sqlite3
import requests, json
from pandas import read_sql_query
import os
from dotenv import load_dotenv

load_dotenv()

class SqlAccess:
    link = "https://myfwcs.fortwayneschools.org/punchcard"
    xapikey = os.getenv("X_API")
    userEndpoint = "/user"
    usersEndpoint = "/users"
    userexistsEndpoint = "/userexists"
    historyEndpoint = "/userhistory"
    clockinEndpoint = "/clockin"
    clockoutEndpoint = "/clockout"

    """
    Allows the User Class to connect to the EasyPunchCard database. 
    """
    def __init__(self, student_id:str):
        """
        Initializes SqlAccess for the user

        Args:
            student_id (str): The student id of the user
        """
        self.student_id = student_id
        self.exists = self.user_exists()
        if self.exists['user_exists']:
            # check if user exists
            self.admin_status = self.exists["admin_status"]
        else:
            # if the user doesn't exist, raise an error
            raise ValueError("User does not exist")
        
    # REMOVE
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
        response = requests.get( self.link + self.userexistsEndpoint + f"?student_id={self.student_id}", headers = {"x-api-key": self.xapikey} )
        jsonValue = json.loads(response.text)
        return jsonValue

    def add_user(self, student_id:str, first_name:str, last_name:str, admin_status:int, graduation_year: int):
        """
        Allows admin users to add users to the database

        Args:
            student_id (str): The student id of the user being added (can't used already)
            first_name (str): The firstname of the user being added to the database
            last_name (str): The lastname of the user being added to the database
            admin_status (int): The admin status of the user being added (only 1 or 0)
            graduation_year (int): The graduation year of the user being added

        Raises:
            ValueError: If the user trying to add another user doesn't have admin status
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        # user is not an admin
        if admin_status == 0:
            data = {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "admin_status": admin_status,
                "graduation_year": graduation_year
            }
            requests.post(self.link + self.userEndpoint, headers={"x-api-key": self.xapikey}, json=data)

        # user is an admin
        elif admin_status == 1:
            data = {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "admin_status": admin_status,
                "graduation_year": 0000
            }
            requests.post(self.link + self.userEndpoint, headers={"x-api-key": self.xapikey}, json=data)

                  
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
        
        requests.delete(self.link + self.userEndpoint + f"?student_id={student_id}", headers={"x-api-key": self.xapikey})


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
        response = requests.get(self.link + self.usersEndpoint, headers={"x-api-key": self.xapikey})
        data = json.loads(response.text)
        return data
    

    def admin_read_user_history(self, student_id:str):
        """
        Allow admin users to retrieve all the data from a specified user table

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
        response = requests.get(self.link + self.historyEndpoint + f"?student_id={student_id}", headers={"x-api-key": self.xapikey})
        data = json.loads(response.text)
        return data    
        

    def get_data_all_users(self, column_name:str):
        """
        allow user to read a single cell from their row on all_users

        Args:
            column_name (str): The column name from the "all_users" table that the data is being retrieved from

        Returns:
            return_type_varies: Returns the data that is retrieved from the specific column on their row on the "all_users" table
        """
        response = requests.get(self.link + self.userEndpoint + f"?student_id={self.student_id}", headers={"x-api-key": self.xapikey})
        data = json.loads(response.text)
        return data[column_name]
    
    
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
        
        response = requests.get(self.link + self.userEndpoint + f"?student_id={student_id}", headers={"x-api-key": self.xapikey})
        data = json.loads(response.text)
        return data[column_name]
    

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
        response = requests.get(self.link + self.userEndpoint + f"?student_id={student_id}", headers={"x-api-key": self.xapikey})
        data = json.loads(response.text)
        return data

    # change to work with the api
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

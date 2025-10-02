import pandas as pd
import requests, json
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
        

    def user_exists(self):
        """
        Checks if the user exists in the database using their student id.

        Returns:
            Dict containing user_exists and admin_status.
        """
        response = requests.get( self.link + self.userexistsEndpoint + f"?student_id={self.student_id}", headers = {"x-api-key": self.xapikey} )
        return json.loads(response.text)


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
    

    def admin_update_historical_data(self, student_id:str, start_time:str, end_time:str):
        """
        allows admin to add historical clockin and clockout data

        Args:
            student_id (str): The student_id of the user who is getting historical data added
            start_time (str): The start time of the 'clock in' In the 'MM/DD/YYYY HH:MM:SS' (24-hour clock) format
            end_time (str): The end time of the 'clock out' In the 'MM/DD/YYYY HH:MM:SS' (24-hour clock) format
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        data={"student_id": student_id, "start_time": start_time, "end_time": end_time}
        requests.post(self.link + self.historyEndpoint, headers={"x-api-key": self.xapikey}, json=data)


    def admin_delete_historical_data(self, student_id:str, start_time:str):
        """
        allows admin to delete historical clockin and clockout data

        Args:
            student_id (str): The student_id of the user who is getting historical data added
            start_time (str): The start time of the 'clock in' In the 'MM/DD/YYYY HH:MM:SS' (24-hour clock) format
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        data={"student_id": student_id, "start_time": start_time}
        print(data)

        print("Getting...")
        r = requests.get(self.link + self.historyEndpoint + f"?student_id={student_id}",
                         headers={"x-api-key": self.xapikey}, json=data)
        print("Status code:", r.status_code)
        print("Response:", r.json())

        print("\nDeleting...")
        r = requests.delete(self.link + self.historyEndpoint + f"?student_id={student_id}",
                        headers={"x-api-key": self.xapikey}, json=data)
        print("Status code:", r.status_code)
        print("Response:", r.text)

        print("\nGetting after deleting...")
        r = requests.get(self.link + self.historyEndpoint + f"?student_id={student_id}",
                         headers={"x-api-key": self.xapikey}, json=data)
        print("Status code:", r.status_code)
        print("Response:", r.json())


    def admin_update_student_data(self, student_id:str, first_name:str=None, last_name:str=None, graduation_year:int=None):
        """
        allows admin to update specific user data

        Args:
            student_id: needed argument
            everything else: not needed (unless want to change)

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        data = {"student_id": student_id, "first_name": first_name, "last_name": last_name, "graduation_year": graduation_year}
        requests.put(self.link + self.userEndpoint, headers={"x-api-key": self.xapikey}, json=data)


    def database_to_excel(self, file_name:str="EasyPunchCard"):
        """
        Export the records from the database to an Excel file.

        Args:
            file_name (str) default = "EasyPunchCard": the name of the file (default is 'EasyPunchCard')

        Raises:
            ValueError: If the user retrieving the data doesn't have admin status
        """
        if self.admin_status == 0:
            raise ValueError("Error: user doesn't have admin status")
        
        documents_path = os.path.expanduser("~/Documents")
        directory = os.path.join(documents_path, "Reports")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        data = self.admin_read_all_users()
        
        df = pd.DataFrame.from_dict(data)
        df.to_excel(f"{directory}/{file_name}.xlsx")

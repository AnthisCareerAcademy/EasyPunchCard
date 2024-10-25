import sqlite3

from database import SqlAccess
from Clock import Clock

class User:
    def __init__(self, unique_id: str, data:dict=None) -> None:
        """if there is data for a new user the data should be a dict with parameters data["username"] and data["admin_status"]"""
        # first check unique_id exists first
        self.access = SqlAccess(unique_id, data["admin_status"])
        # if so it'll use data from the db
        if self.access.exists:
            print(f"{sqlite3.IntegrityError}: student_id already exists in table")
            self.clock = Clock(unique_id)

        else:
            # if there is data use the data to create another user
            if data is not None:
                self.access.add_self(data["username"])
                self.clock = Clock(unique_id)
            else:
                raise 'ERROR: data["admin_status"] needs to be an INT'

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id} has {self.current_hours} hrs and their last clock action was {self.last_clock_action}"
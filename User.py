import sqlite3

from database import SqlAccess

class User:
    def __init__(self, unique_id: str, data:dict=None) -> None:
        # TODO first check unique_id exists first
        self.access = SqlAccess(unique_id, data["admin_status"])
        # if so it'll use data from the db
        if self.access.exists:
            print(f"{sqlite3.IntegrityError}: student_id already exists in table")

        else:
            # if there is data use the data to create another user
            if data is not None:
                self.access.add_self(data["username"])
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id}"
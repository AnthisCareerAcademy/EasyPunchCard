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

        

        # else raise error because no data was provided to create user

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id}"

data = {"username": "AungAung", "admin_status": 1}
admin = User("1234", data)
print(admin.access.read_all_users())
print(admin.access.read_user_table('1222'))
print(admin.access.read_user_table('4567'))
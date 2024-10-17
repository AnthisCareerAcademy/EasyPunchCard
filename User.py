import sqlite3

from database import SqlAccess

class User:
    def __init__(self, first_name: str, last_name: str, unique_id: str, admin_status: int) -> None:
        # first check unique_id exists first
        self.first_name = first_name
        self.last_name = last_name
        self.unique_id = unique_id
        self.admin_status = admin_status
        self.access = SqlAccess(self.admin_status) 

        # attempt to add user
        try:
            self.access.add_self(self.unique_id, f"{self.first_name}{self.last_name}")
        except sqlite3.IntegrityError as e:
            print(f"{e}: student_id already exists in table")

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id}"

admin = User("Logan", "Ghast", "1234", 1)
print(admin.access.read_all_users())
print(admin.access.read_user_table('12'))
print(admin.access.read_user_table('4567'))
import sqlite3

from database import SqlAccess

class User:
    def __init__(self, first_name: str, last_name: str, unique_id: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.unique_id = unique_id
        self.access = SqlAccess()
        try:
            self.access.add_user(self.unique_id, f"{self.first_name}{self.last_name}", 0)
        except sqlite3.IntegrityError as e:
            print(f"{e}: student_id already exists in table")

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id}"

User("martin", "carapia", "fee")
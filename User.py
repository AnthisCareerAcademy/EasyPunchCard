import sqlite3
from reports import Report
from database import SqlAccess
from Clock import Clock

class User:
    """User class interacts with the SqlAccess and Clock class if the user isn't admin"""
    
    # default admin is unique_id = 0000
    def __init__(self, unique_id: str) -> None:
        # first check unique_id exists first
        self.access = SqlAccess(unique_id)
        if self.access.exists:
            # if the user exists, give user access to clock class
            if self.access.admin_status != 1:
                # and if user isn't admin
                self.clock = Clock(unique_id)
            elif self.access.admin_status == 1:
                # if admin
                self.report = Report(unique_id)

    
    def __str__(self) -> str:
        return f"User: {self.unique_id}"
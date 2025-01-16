import requests
from database import SqlAccess

class Clock:
    """
    Clock class will allow User to clock in or clock out and record the time spent between
    Execute the close method after done using Clock class

    Attributes:
        id (str): The unique identifier (student_id) for the user.
        access (SqlAccess): An instance of the SqlAccess class that manages the user's data and database access.

    Args:
        student_id (str): The ID of the student using the clocking system.
    """
    def __init__(self, student_id: str) -> None:
        """
        Initializes the clock class for a specific user

        Args:
            student_id (str): The ID of the student clocking in/out.
        
        Initializes the `access` attribute, which provides access to the user's database records.
        """
        self.id = student_id
        self.access = SqlAccess(student_id)


    def clock_in(self):
        """
        Clocks the user in if they aren't already clocked in

        - Checks if the user is already clocked in (working_status = 1).
        - Inserts a record in the user's specific table (`user_{student_id}`) with the clock-in time.
        - Updates the user's `working_status` to 1 and stores the start time in the `all_users` table.
        """
        requests.post(self.access.link + self.access.clockinEndpoint, headers={"x-api-key": self.access.xapikey}, json={"student_id": self.id})
    

    def clock_out(self):
        """
        Clocks the user out if they aren't already clocked out
        
        - Checks if the user has a start time recorded. If not, the user is already clocked out.
        - Calculates the time worked and updates the user's table with the end time and total minutes worked.
        - Resets the start time and updates the `working_status` and `total_minutes` in the `all_users` table.
        """
        requests.post(self.access.link + self.access.clockoutEndpoint, headers={"x-api-key": self.access.xapikey}, json={"student_id": self.id})
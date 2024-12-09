from reports import Report
from database import SqlAccess
from Clock import Clock

class User:
    """
    User class interacts with the SqlAccess and Clock class if the user isn't admin

    Attributes:
        access (SqlAccess): An instance of the SqlAccess class to manage user data and access.
        clock (Clock, optional): An instance of the Clock class for non-admin users to track time.
        report (Report, optional): An instance of the Report class for admin users to generate reports.

    Args:
        unique_id (str): A unique identifier (such as a student ID) for the user.
    
    Raises:
        ValueError: If the user does not exist in the database.
    """
    
    # default admin is unique_id = 0000
    def __init__(self, unique_id: str) -> None:
        """
        Initialize a new User object and check if the user exists in the database.

        Depending on the user's admin status, the appropriate classes are instantiated:
        - Non-admin users will have access to the Clock class.
        - Admin users will have access to the Report class.

        Args:
            unique_id (str): The unique identifier of the user to be checked and given access.

        Raises:
            ValueError: If the user with the provided `unique_id` does not exist in the system.
        """
        # first check unique_id exists first
        self.access = SqlAccess(unique_id)
        if self.access.exists:
            # if the user exists, give user access to clock class
            if self.access.admin_status == 0:
                # and if user isn't admin
                self.clock = Clock(unique_id)
            elif self.access.admin_status == 1:
                # if admin
                self.report = Report(unique_id)

    
    def __str__(self) -> str:
        """
        Return a string representation of the User object, showing the unique ID.

        Returns:
            str: A string in the format "User: {unique_id}".
        """
        return f"User: {self.unique_id}"
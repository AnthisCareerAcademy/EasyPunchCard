class User:
    def __init__(self, first_name: str, last_name: str, unique_id: str, is_admin: bool = False, current_hours: float = 0.0, last_clock_action: str = "") -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.unique_id = unique_id
        self.is_admin = is_admin
        self.current_hours = current_hours
        self.last_clock_action = last_clock_action

    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id} has {self.current_hours} hrs and their last clock action was {self.last_clock_action}"
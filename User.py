class User:
    def __init__(self, first_name: str, last_name: str, unique_id: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.unique_id = unique_id
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} with Unique ID {self.unique_id}"
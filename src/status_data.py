from __future__ import annotations

statuses = [
    "planned",
    "watching",
    "dropped",
    "finished",
]

class Status:
    def __init__(self, id: int = 0) -> None:
        assert isinstance(id, int)
        self.id = id
    
    def __str__(self) -> str:
        return statuses[self.id]
    
    def from_str(self, status: str) -> Status:
        assert status in statuses, f"Status '{status}' in not a valid option"
        new_id = statuses.index(status)
        self.id = new_id
        return self
    
    def to_str(self) -> str:
        return str(self)

PLANNED  = Status().from_str("planned")
WATCHING = Status().from_str("watching")
DROPPED  = Status().from_str("dropped")
FINISHED = Status().from_str("finished")

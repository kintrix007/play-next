from __future__ import annotations

STATUS_STRINGS = [
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
        return STATUS_STRINGS[self.id]
    
    def from_str(self, status: str) -> Status:
        assert isinstance(status, str)
        assert status in STATUS_STRINGS, f"Status '{status}' is not a valid status"
        self.id = STATUS_STRINGS.index(status)
        return self
    
    def to_str(self) -> str:
        return str(self)
    
    def __eq__(self, s: Status) -> bool:
        return STATUS_STRINGS[self.id] == STATUS_STRINGS[s.id]
    
    def __ne__(self, s: Status) -> bool:
        return STATUS_STRINGS[s.id] != STATUS_STRINGS[s.id]

PLANNED  = Status().from_str("planned")
WATCHING = Status().from_str("watching")
DROPPED  = Status().from_str("dropped")
FINISHED = Status().from_str("finished")

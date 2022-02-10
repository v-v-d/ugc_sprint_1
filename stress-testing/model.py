from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    id: int
    user_id: int
    timestamp: int
    move_id: int

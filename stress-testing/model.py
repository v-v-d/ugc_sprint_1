from pydantic import BaseModel


class Data(BaseModel):
    id: int
    user_id: int
    timestamp: int
    move_id: int


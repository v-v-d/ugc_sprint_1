from pydantic import BaseModel, UUID4


class FilmProgressInputSchema(BaseModel):
    user_id: UUID4
    progress: int
    total: int

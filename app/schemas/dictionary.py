from pydantic import BaseModel


# Shared properties
class Dictionary(BaseModel):
    id: int
    english: str
    russian: str

    class Config:
        orm_mode = True

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    first_name: str

    class Config:
        orm_mode = True


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    message_id: int
    user: Optional[User]
    chat: Optional[Chat]
    text: str

    class Config:
        fields = {
            'user': 'from'
        }


class Update(BaseModel):
    message: Optional[Message]

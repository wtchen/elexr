from pydantic import BaseModel


class Message(BaseModel):
    message: str = "Server error"

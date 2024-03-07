from pydantic import BaseModel


class User(BaseModel):
    uid: str
    phoneNumber: int
    name: str
    address: str

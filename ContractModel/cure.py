from pydantic import BaseModel


class Cure(BaseModel):
    uid: str
    name: str
    description: str
    price: int
    count: int
    availabilityTime: int

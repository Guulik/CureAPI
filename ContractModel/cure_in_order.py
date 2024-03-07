from pydantic import BaseModel


class CureInOrder(BaseModel):
    name: str
    count: int
    price: int
    delivery_time: int

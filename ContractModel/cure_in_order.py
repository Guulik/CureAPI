from pydantic import BaseModel


class CureInOrder(BaseModel):
    name: str
    count: int
    price: int
    delivery_time: int
    cure_id: int
    user_id: int
    order_id: int | None

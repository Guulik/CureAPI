from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    uid: str
    id: int
    price_sum: int
    delivery_type: bool
    timestamp: datetime

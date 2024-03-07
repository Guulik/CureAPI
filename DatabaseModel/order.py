from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from db_context import Base
from DatabaseModel.cure_in_order import CureInOrder

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="order")
    price_sum = Column(Integer)
    delivery_type = Column(Boolean)
    timestamp = Column(DateTime)

    cure_in_order = relationship('CureInOrder', back_populates='order')
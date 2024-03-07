from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_context import Base

class CureInOrder(Base):
    __tablename__ = 'cure_in_order'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    count = Column(Integer)
    price = Column(Integer)
    delivery_time = Column(Integer)

    cure_id = Column(String, ForeignKey('cures.id'))
    cure = relationship("Cure", back_populates="cure_in_order")
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship("User", back_populates="cure_in_order")
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    order = relationship("Order", back_populates="cure_in_order")

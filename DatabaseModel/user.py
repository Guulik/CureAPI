from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_context import Base
from DatabaseModel.order import Order
from DatabaseModel.cure_in_order import CureInOrder

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # с uid через string просто проще работать, потому что через UUID он в базе сохраняет без дефисов
    uid = Column(String, unique=True, nullable=False)
    phoneNumber = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String)

    order = relationship("Order", back_populates="user")
    cure_in_order = relationship("CureInOrder", back_populates="user")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_context import Base


class Cure(Base):
    __tablename__ = 'cures'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    count = Column(Integer)
    availabilityTime = Column(Integer)

    cure_in_order = relationship('CureInOrder', back_populates='cure')
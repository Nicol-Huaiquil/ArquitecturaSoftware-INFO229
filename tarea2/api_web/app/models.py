from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text,Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import ast
from .database import Base #Se importa el objeto Base desde el archivo database.py

class User(Base): 

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(100), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
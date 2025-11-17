# backend/app/model.py
import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    vin = Column(String, unique=True, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    battery_capacity_kwh = Column(Float, nullable=False)

# backend/app/crud.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import model, schemas   # ✅ notice: .model, NOT .models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------ PASSWORD UTILS ------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------ USER CRUD ------------

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = hash_password(user_in.password)
    user = model.User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ------------ VEHICLE CRUD ------------

def create_vehicle(db: Session, user_id: str, vehicle_in: schemas.VehicleCreate):
    v = model.Vehicle(
        user_id=user_id,
        vin=vehicle_in.vin,
        make=vehicle_in.make,
        model=vehicle_in.model,
        model_year=vehicle_in.model_year,
        battery_capacity_kwh=vehicle_in.battery_capacity_kwh,
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def get_vehicle(db: Session, vehicle_id: str):
    return db.query(model.Vehicle).filter(model.Vehicle.id == vehicle_id).first()

# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------------------- USER --------------------
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=6)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


# -------------------- VEHICLE --------------------
class VehicleCreate(BaseModel):
    vin: str
    make: str
    model: str
    model_year: int
    battery_capacity_kwh: float


class VehicleOut(VehicleCreate):
    id: str
    user_id: Optional[str]

    class Config:
        from_attributes = True


# -------------------- TELEMETRY --------------------
class TelemetryIn(BaseModel):
    vehicle_id: str
    battery_level: float
    speed: float
# -------------------- RANGE PREDICTION INPUT --------------------
class RangePredictIn(BaseModel):
    battery_level: float
    speed: float
    temperature: float


# -------------------- CHATBOT INPUT --------------------
class ChatbotIn(BaseModel):
    message: str

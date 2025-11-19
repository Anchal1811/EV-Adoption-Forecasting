from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import redis
import os
import json

from dotenv import load_dotenv

# Force load the .env from the project root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(env_path)

print("🔑 Loaded GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

from . import db, schemas, crud, auth
from .forecast_service import train_and_forecast
from .range_predictor import predict_range
from .settings import settings

# ---------- CREATE TABLES ----------
db.Base.metadata.create_all(bind=db.engine)

# ---------- FASTAPI APP ----------
app = FastAPI(title="EV Backend API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB SESSION ----------
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

# ============================================================
#                           REDIS
# ============================================================

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    r = redis.Redis.from_url(REDIS_URL)
    r.ping()
    print("✅ Redis Connected")
except:
    print("⚠️ Redis NOT Connected — Using fallback (disabled)")
    r = None


# ============================================================
#                         AUTH ROUTES
# ============================================================

@app.post("/api/v1/auth/register", response_model=schemas.UserOut)
def register_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = crud.get_user_by_email(db, u.email)
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, u)


@app.post("/api/v1/auth/login")
def login_user(u: schemas.LoginIn, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, u.email)

    if not user or not crud.verify_password(u.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token(subject=user.id)
    return {"access_token": token}


# ============================================================
#                    VEHICLE ROUTES
# ============================================================

@app.post("/api/v1/vehicles", response_model=schemas.VehicleOut)
def create_vehicle(v: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db, None, v)


@app.get("/api/v1/vehicles/{vehicle_id}", response_model=schemas.VehicleOut)
def read_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    vehicle = crud.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


# ============================================================
#                    TELEMETRY ROUTE
# ============================================================

@app.post("/api/v1/telemetry")
def telemetry_ingest(payload: schemas.TelemetryIn):
    if not r:
        raise HTTPException(status_code=500, detail="Redis unavailable")

    r.lpush("telemetry_queue", json.dumps(payload.dict(), default=str))
    return {"status": "queued"}


# ============================================================
#                        FORECAST API
# ============================================================

@app.get("/api/v1/forecast")
def forecast():
    try:
        data = train_and_forecast()
        return {"status": "success", "forecast": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
#                   EV RANGE PREDICTION API
# ============================================================

@app.post("/api/v1/range/predict")
def ev_range_prediction(data: schemas.RangePredictIn):
    try:
        result = predict_range(
            battery_level=data.battery_level,
            speed=data.speed,
            temperature=data.temperature,
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
#                     EV CHATBOT (GEMINI)
# ============================================================
# ============================================================
#                     EV CHATBOT (GEMINI)
# ============================================================

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/api/v1/chatbot")
def chatbot(ev_input: schemas.ChatbotIn):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")   # <-- FIXED MODEL
        response = model.generate_content(ev_input.message)

        reply = getattr(response, "text", None)
        if not reply:
            reply = response.candidates[0].content.parts[0].text

        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini ERROR → {str(e)}")

     
    

# ============================================================
#                         ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "🚗⚡ EV Forecasting Backend is running!",
        "docs": "/docs",
        "api_base": "/api/v1",
    }

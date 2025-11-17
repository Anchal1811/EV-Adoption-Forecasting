# backend/app/range_predictor.py

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = "backend/app/models/range_model.pkl"
DATA_PATH = "backend/app/data/ev_data.csv"


def train_range_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Telemetry dataset missing: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Your ev_data.csv has: battery_level, speed, temperature, energy_consumption
    # If estimated_range_km is NOT present, we create a synthetic target column.
    if "estimated_range_km" not in df.columns:
        base_range = 4 * df["battery_level"]             # more battery → more range
        speed_penalty = 0.5 * df["speed"]                # higher speed reduces range
        temp_penalty = 0.3 * (df["temperature"] - 25).abs()  # too hot/cold reduces range

        est_range = base_range - speed_penalty - temp_penalty
        df["estimated_range_km"] = est_range.clip(lower=20, upper=500)

    X = df[["battery_level", "speed", "temperature"]]
    y = df["estimated_range_km"]

    model = RandomForestRegressor(n_estimators=120, random_state=42)
    model.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model


def load_range_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_range_model()


def predict_range(battery_level: float, speed: float, temperature: float):
    model = load_range_model()

    input_data = [[battery_level, speed, temperature]]
    predicted_km = model.predict(input_data)[0]

    return {
        "estimated_range_km": round(float(predicted_km), 2),
        "battery_level": battery_level,
        "speed": speed,
        "temperature": temperature,
    }

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

MODEL_PATH = "backend/app/models/ev_model.pkl"

def load_data():
    """
    Load EV telemetry data from CSV/DB/Redis.
    Replace this function with your actual data source.
    """
    # Example: read from CSV
    df = pd.read_csv("backend/app/data/ev_data.csv")
    return df

def train_model():
    """
    Train a RandomForest model and save it to disk.
    """
    df = load_data()
    X = df[["battery_level", "speed", "temperature"]]
    y = df["energy_consumption"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    """
    Load the trained model from disk, or train if it doesn't exist.
    """
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = train_model()
    return model

def forecast_next(model, last_row, steps=5):
    """
    Forecast energy consumption for the next N steps
    """
    forecast = []
    for _ in range(steps):
        pred = model.predict(last_row)[0]
        forecast.append(round(pred, 2))
        # Example: decrement battery level for next prediction
        last_row[0][0] = max(last_row[0][0] - 1, 0)
    return forecast

def train_and_forecast():
    """
    Load or train model, then forecast using the last row of data.
    """
    df = load_data()
    model = load_model()
    last_row = df[["battery_level", "speed", "temperature"]].iloc[-1].values.reshape(1, -1)
    return forecast_next(model, last_row)

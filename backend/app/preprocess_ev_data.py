import pandas as pd
import numpy as np
import os

RAW_PATH = "backend/app/data/ev_data.csv"          # your raw dataset
OUTPUT_DIR = "backend/app/output"                  # <-- output folder
CLEAN_PATH = f"{OUTPUT_DIR}/clean_ev_data.csv"     # cleaned dataset path

def preprocess_ev_data():

    print("🔧 Loading raw data...")
    df = pd.read_csv(RAW_PATH)

    # -------------------------------------
    # Ensure output folder exists
    # -------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # -------------------------------------
    # Required Columns
    # -------------------------------------
    required = ["battery_level", "speed", "temperature", "energy_consumption"]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")

    df = df[required]

    # -------------------------------------
    # Drop duplicates
    # -------------------------------------
    df = df.drop_duplicates()

    # -------------------------------------
    # Fill missing values
    # -------------------------------------
    df = df.fillna({
        "battery_level": df["battery_level"].median(),
        "speed": df["speed"].median(),
        "temperature": df["temperature"].median(),
        "energy_consumption": df["energy_consumption"].median(),
    })

    # -------------------------------------
    # Convert types
    # -------------------------------------
    df = df.astype({
        "battery_level": float,
        "speed": float,
        "temperature": float,
        "energy_consumption": float
    })

    # -------------------------------------
    # Remove impossible values
    # -------------------------------------
    df = df[
        (df.battery_level >= 0) & (df.battery_level <= 100) &
        (df.speed >= 0) & (df.speed <= 200) &
        (df.temperature >= -30) & (df.temperature <= 60)
    ]

    # -------------------------------------
    # Remove statistical outliers
    # -------------------------------------
    for col in required:
        q1 = df[col].quantile(0.10)
        q3 = df[col].quantile(0.90)
        df = df[(df[col] >= q1) & (df[col] <= q3)]

    # -------------------------------------
    # Shuffle
    # -------------------------------------
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # -------------------------------------
    # Save cleaned file
    # -------------------------------------
    df.to_csv(CLEAN_PATH, index=False)
    print(f"✅ Cleaned dataset saved to: {CLEAN_PATH}")

    return df


if __name__ == "__main__":
    preprocess_ev_data()

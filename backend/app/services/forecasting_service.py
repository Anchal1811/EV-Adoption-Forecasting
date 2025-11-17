import pandas as pd
from sklearn.linear_model import LinearRegression

def train_and_forecast():
    df = pd.read_csv("data/ev_population.csv")   # your dataset location

    df_grouped = df.groupby("Model Year")["VIN (1-10)"].count().reset_index()
    df_grouped.columns = ["year", "count"]

    X = df_grouped[["year"]]
    y = df_grouped["count"]

    model = LinearRegression()
    model.fit(X, y)

    next_year = int(df_grouped["year"].max() + 1)
    prediction = model.predict([[next_year]])[0]

    return {
        "year": next_year,
        "forecast": float(prediction),
        "model": "LinearRegression"
    }

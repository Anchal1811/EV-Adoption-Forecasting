# train_model.py
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Step 1: Load Dataset
df = pd.read_csv("./data/Electric_Vehicle_Population_Data.csv")


# Step 2: Preprocess Data
# Convert 'Model Year' to datetime format for forecasting
df['Model Year'] = pd.to_datetime(df['Model Year'], format='%Y')

# Aggregate data: Count number of EVs per year
yearly_data = df.groupby(df['Model Year'].dt.year).size().reset_index(name='EV_Count')

# Prepare data for Prophet
data = pd.DataFrame()
data['ds'] = pd.to_datetime(yearly_data['Model Year'], format='%Y')
data['y'] = yearly_data['EV_Count']

# Step 3: Initialize Prophet model
model = Prophet(yearly_seasonality=True)
model.fit(data)

# Step 4: Forecast next 5 years
future = model.make_future_dataframe(periods=5, freq='Y')
forecast = model.predict(future)

# Step 5: Save the forecasted data
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('forecast_output.csv', index=False)

# Step 6: Visualize forecast
model.plot(forecast)
plt.title('Electric Vehicle Adoption Forecast')
plt.xlabel('Year')
plt.ylabel('EV Count')
plt.show()

print("✅ Model training complete! Forecast saved to 'forecast_output.csv'")

# Save forecast
forecast.to_csv("data/forecast_results.csv", index=False)

# Save trained model
import joblib
joblib.dump(model, "models/ev_forecast_model.pkl")

print("✅ Forecast saved to data/forecast_results.csv")
print("✅ Model saved to models/ev_forecast_model.pkl")


# Save forecast results and model
import joblib
forecast.to_csv("data/forecast_results.csv", index=False)
joblib.dump(model, "models/ev_forecast_model.pkl")

print("✅ Forecast saved to data/forecast_results.csv")
print("✅ Model saved to models/ev_forecast_model.pkl")


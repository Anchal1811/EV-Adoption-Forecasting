from fastapi import APIRouter
from app.ml.model import EVForecastModel

router = APIRouter()
model = EVForecastModel()

@router.post("/forecast")
def forecast_ev(data: dict):
    prediction = model.forecast(data)
    return {"prediction": prediction}

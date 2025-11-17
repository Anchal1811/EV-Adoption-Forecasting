from pydantic import BaseModel

class ForecastOut(BaseModel):
    year: int
    forecast_value: float
    model_used: str

    class Config:
        orm_mode = True

import time
from redis import Redis
import json
from app.ml.model import EVForecastModel

redis = Redis(host="redis", port=6379)
model = EVForecastModel()

def run_forecast_job(job_id, payload):
    # Long job simulation
    time.sleep(3)

    result = model.forecast(payload)

    redis.set(job_id, json.dumps({"status": "completed", "result": result}))

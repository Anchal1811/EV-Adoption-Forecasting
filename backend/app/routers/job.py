from fastapi import APIRouter
from redis import Redis
import uuid
import json

router = APIRouter()
redis = Redis(host="redis", port=6379)

@router.post("/jobs/create")
def submit_job(payload: dict):
    job_id = str(uuid.uuid4())

    redis.rpush("jobs", json.dumps({
        "job_id": job_id,
        "payload": payload
    }))

    return {"job_id": job_id, "status": "queued"}

@router.get("/jobs/{job_id}")
def get_status(job_id: str):
    data = redis.get(job_id)
    if not data:
        return {"status": "pending"}
    return json.loads(data.decode())

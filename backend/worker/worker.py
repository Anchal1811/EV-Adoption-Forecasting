import os
import redis
import json
import time
import psycopg2
from datetime import datetime
from psycopg2.extras import Json

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5433/evdb")

r = redis.from_url(REDIS_URL)

def insert_telemetry(conn, t):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO telemetry (time, vehicle_id, vin, latitude, longitude, speed_kph, soc_percent, power_kw, extra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            t.get("time") or datetime.utcnow(),
            t.get("vehicle_id"),
            t.get("vin"),
            t.get("latitude"),
            t.get("longitude"),
            t.get("speed_kph"),
            t.get("soc_percent"),
            t.get("power_kw"),
            Json(t.get("extra") or {})
        ))
    conn.commit()

def main():
    conn = psycopg2.connect(DATABASE_URL)
    while True:
        item = r.rpop("telemetry_queue")
        if not item:
            time.sleep(0.5)
            continue
        try:
            t = json.loads(item)
            if isinstance(t.get("time"), str):
                try:
                    t["time"] = datetime.fromisoformat(t["time"].replace("Z", "+00:00"))
                except:
                    t["time"] = datetime.utcnow()
            insert_telemetry(conn, t)
            print("Inserted telemetry:", t.get("vin") or t.get("vehicle_id"))
        except Exception as e:
            print("Worker error:", e)

if __name__ == "__main__":
    main()

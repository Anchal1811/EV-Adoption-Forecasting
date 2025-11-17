-- init.sql: run once on DB start
CREATE EXTENSION IF NOT EXISTS "timescaledb";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  password_hash TEXT,
  role TEXT DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Vehicles
CREATE TABLE IF NOT EXISTS vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  vin TEXT UNIQUE,
  make TEXT,
  model TEXT,
  model_year INT,
  battery_capacity_kwh NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Telemetry table (timescale hypertable)
CREATE TABLE IF NOT EXISTS telemetry (
  time TIMESTAMPTZ NOT NULL,
  vehicle_id UUID NOT NULL,
  vin TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  speed_kph NUMERIC,
  soc_percent NUMERIC,
  power_kw NUMERIC,
  extra JSONB
);
SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE);

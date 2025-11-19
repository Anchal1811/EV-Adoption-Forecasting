"use client";
import { useState } from "react";
import { api } from "@/utils/api";

export default function Range() {
  const [battery, setBattery] = useState("");
  const [speed, setSpeed] = useState("");
  const [temp, setTemp] = useState("");
  const [res, setRes] = useState(null);

  const predict = async () => {
    const data = await api("/range/predict", "POST", {
      battery_level: Number(battery),
      speed: Number(speed),
      temperature: Number(temp),
    });
    setRes(data.result);
  };

  return (
    <div className="card max-w-xl mx-auto">
      <h1 className="text-xl font-bold mb-3">EV Range Predictor</h1>

      <input className="input" placeholder="Battery %" onChange={(e)=>setBattery(e.target.value)} />
      <br /><br />
      <input className="input" placeholder="Speed" onChange={(e)=>setSpeed(e.target.value)} />
      <br /><br />
      <input className="input" placeholder="Temperature" onChange={(e)=>setTemp(e.target.value)} />
      
      <br /><br />
      <button className="btn-primary w-full" onClick={predict}>Predict</button>

      {res && (
        <div className="mt-4 p-4 bg-blue-50 border rounded-lg">
          <p className="font-semibold">Estimated Range: {res} km</p>
        </div>
      )}
    </div>
  );
}

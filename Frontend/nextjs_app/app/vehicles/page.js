"use client";
import { useState } from "react";
import { api } from "@/utils/api";

export default function Vehicles() {
  const [model, setModel] = useState("");
  const [battery, setBattery] = useState("");

  const save = async () => {
    const token = localStorage.getItem("token");
    await api("/vehicles", "POST", { model, battery_capacity: battery }, token);
    alert("Vehicle added!");
  };

  return (
    <div className="card max-w-xl mx-auto">
      <h1 className="text-xl font-bold mb-3">Add New Vehicle</h1>

      <input className="input" placeholder="Model" onChange={(e)=>setModel(e.target.value)} />
      <br /><br />
      <input className="input" placeholder="Battery Capacity" onChange={(e)=>setBattery(e.target.value)} />

      <br /><br />
      <button className="btn-primary w-full" onClick={save}>Save</button>
    </div>
  );
}

"use client";
import { useState } from "react";
import { api } from "@/utils/api";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Forecast() {
  const [data, setData] = useState([]);

  const load = async () => {
    const res = await api("/forecast");
    setData(res.forecast);
  };

  return (
    <div className="card">
      <h1 className="text-xl font-bold">Energy Forecast Chart</h1>

      <button className="btn-primary mt-3" onClick={load}>Load Data</button>

      {data.length > 0 && (
        <div className="mt-5">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#2563eb" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

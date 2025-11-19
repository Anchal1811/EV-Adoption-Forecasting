"use client";
import { useState } from "react";
import { api } from "@/utils/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");

  const login = async () => {
    const res = await api("/auth/login", "POST", { email, password: pwd });
    localStorage.setItem("token", res.access_token);
    alert("Login successful!");
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-xl">
      <h1 className="text-2xl font-bold mb-4">Login</h1>

      <input className="input" placeholder="Email" onChange={(e)=>setEmail(e.target.value)} />
      <br /><br />
      <input className="input" placeholder="Password" type="password" onChange={(e)=>setPwd(e.target.value)} />

      <br /><br />
      <button className="btn-primary w-full" onClick={login}>Login</button>
    </div>
  );
}

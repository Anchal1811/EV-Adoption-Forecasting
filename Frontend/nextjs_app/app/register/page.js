"use client";
import { useState } from "react";
import { api } from "@/utils/api";
import Navbar from "@/components/Navbar";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPwd] = useState("");

  const register = async () => {
    try {
      await api("/auth/register", "POST", { email, password });
      alert("User Registered!");
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="p-6">
        <h1 className="text-xl font-bold mb-3">Register</h1>

        <input className="border p-2" placeholder="Email"
          onChange={(e)=>setEmail(e.target.value)} />

        <input className="border p-2 ml-2" type="password" placeholder="Password"
          onChange={(e)=>setPwd(e.target.value)} />

        <button className="bg-green-600 text-white px-4 py-2 ml-3"
          onClick={register}>
          Register
        </button>
      </div>
    </div>
  );
}

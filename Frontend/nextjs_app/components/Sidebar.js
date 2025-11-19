"use client";

import { useState } from "react";
import { motion } from "framer-motion";

export default function Sidebar() {
  const [open, setOpen] = useState(true);

  return (
    <motion.div
      animate={{ width: open ? 240 : 70 }}
      className="h-screen bg-black text-white p-5 fixed left-0 top-0 shadow-xl"
    >
      <button
        onClick={() => setOpen(!open)}
        className="text-white mb-5"
      >
        {open ? "<" : ">"}
      </button>

      <nav className="space-y-3">
        <a href="/" className="block hover:text-blue-400">🏠 Home</a>
        <a href="/login" className="block hover:text-blue-400">🔐 Login</a>
        <a href="/register" className="block hover:text-blue-400">📝 Register</a>
        <a href="/vehicles" className="block hover:text-blue-400">🚗 Vehicles</a>
        <a href="/predict-range" className="block hover:text-blue-400">🔋 Range</a>
        <a href="/forecast" className="block hover:text-blue-400">📊 Forecast</a>
        <a href="/chatbot" className="block hover:text-blue-400">🤖 Chatbot</a>
      </nav>
    </motion.div>
  );
}

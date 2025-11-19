"use client";
import { useState } from "react";
import { api } from "@/utils/api";

export default function Chatbot() {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);

  const send = async () => {
    if (!msg.trim()) return;

    setChat((c) => [...c, { sender: "user", text: msg }]);

    const res = await api("/chatbot", "POST", { message: msg });

    setChat((c) => [...c, { sender: "user", text: msg }, { sender: "bot", text: res.reply }]);
    setMsg("");
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-xl p-6 shadow-xl">
      <h1 className="text-2xl font-bold mb-4">EV Assistant 🤖</h1>

      <div className="h-[400px] overflow-y-auto p-4 bg-gray-50 rounded-lg border">
        {chat.map((m, i) => (
          <div
            key={i}
            className={`p-3 my-2 rounded-xl max-w-xs ${
              m.sender === "user"
                ? "bg-blue-600 text-white ml-auto"
                : "bg-gray-200"
            }`}
          >
            {m.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2 mt-3">
        <input
          className="input flex-1"
          value={msg}
          placeholder="Ask something..."
          onChange={(e) => setMsg(e.target.value)}
        />
        <button className="btn-primary" onClick={send}>Send</button>
      </div>
    </div>
  );
}

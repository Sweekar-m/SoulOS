import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { motion } from "framer-motion";
import "./styles.css";

type Health = { status: string; service: string; version: string };
const apiBase = (import.meta.env.VITE_SOULOS_API_URL ?? "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`${apiBase}/health`)
      .then((r) => { if (!r.ok) throw new Error(`Backend returned ${r.status}`); return r.json() as Promise<Health>; })
      .then(setHealth)
      .catch((e: Error) => setError(e.message));
  }, []);

  return <main className="shell">
    <aside><div className="brand">soulOS</div><nav><button className="active">Chat</button><button>Tools</button><button>Memory</button><button>Settings</button></nav></aside>
    <section className="workspace">
      <header><div><span className="eyebrow">DESKTOP AGENT</span><h1>What can I do for you?</h1></div><span className={`status ${health ? "online" : ""}`}>{health ? "Backend online" : "Connecting…"}</span></header>
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="welcome"><p>Local orchestration is ready. Commands are classified before tools or models are selected.</p>{error && <small>Connection error: {error}</small>}</motion.div>
      <div className="composer"><textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Ask SoulOS anything…"/><button disabled={!message.trim()}>Send</button></div>
    </section>
  </main>;
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);

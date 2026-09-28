import { FormEvent, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "../lib/api";
import type { ChatResponse, ConversationMessage, Health } from "../lib/types";

export function AppShell() {
  const [health, setHealth] = useState<Health | null>(null);
  const [message, setMessage] = useState("");
  const [sessionId, setSessionId] = useState<string>();
  const [reply, setReply] = useState<ChatResponse>();
  const [history, setHistory] = useState<ConversationMessage[]>([]);
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.health().then(setHealth).catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!sessionId) return;
    api.conversation(sessionId).then((conversation) => setHistory(conversation.messages)).catch(() => undefined);
  }, [sessionId]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!message.trim() || busy) return;
    setBusy(true);
    setError(undefined);
    try {
      const result = await api.chat(message.trim(), sessionId);
      setSessionId(result.session_id);
      setReply(result);
      setHistory((current) => [
        ...current,
        { role: "user", content: message.trim(), created_at: new Date().toISOString() },
        { role: "assistant", content: result.response, created_at: new Date().toISOString() },
      ]);
      setMessage("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <aside>
        <div className="brand">soulOS</div>
        <nav><button className="active">Chat</button><button>Tools</button><button>Memory</button><button>Settings</button></nav>
        <div className="side-status">{health ? "● Connected" : "○ Connecting"}</div>
      </aside>
      <section className="workspace">
        <header>
          <div><span className="eyebrow">DESKTOP AGENT</span><h1>What can I do for you?</h1></div>
          <span className={`status ${health ? "online" : ""}`}>{health ? "Backend online" : "Connecting…"}</span>
        </header>
        <motion.section initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="conversation">
          {history.length ? history.map((item, index) => (
            <article key={`${item.created_at}-${index}`} className={item.role === "user" ? "user" : "assistant"}>
              <div className="meta">{item.role}</div><p>{item.content}</p>
            </article>
          )) : <p className="empty">Local orchestration is ready. Commands are classified before tools or models are selected.</p>}
          {error && <small className="error">{error}</small>}
        </motion.section>
        <form className="composer" onSubmit={submit}>
          <textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Ask SoulOS anything…" disabled={busy}/>
          <button disabled={!message.trim() || busy}>{busy ? "Thinking…" : "Send"}</button>
        </form>
      </section>
    </main>
  );
}

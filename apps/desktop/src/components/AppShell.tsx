import { FormEvent, useState } from "react";
import { motion } from "framer-motion";
import { ChatView } from "./ChatView";
import { CommandPalette } from "./CommandPalette";
import { ModelSelector } from "./ModelSelector";
import { Settings } from "./Settings";
import { Sidebar } from "./Sidebar";
import { SystemStatus } from "./SystemStatus";
import { ToolActivity } from "./ToolActivity";
import { useChat } from "../hooks/useChat";
import { useHealth } from "../hooks/useHealth";
import { useModels } from "../hooks/useModels";
import { normalizeToolEvents } from "../lib/toolEvents";

export function AppShell() {
  const [active, setActive] = useState<"Chat" | "Tools" | "Memory" | "Settings">("Chat");
  const [message, setMessage] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const apiUrl = import.meta.env.VITE_SOULOS_API_URL ?? "http://127.0.0.1:8000/api/v1";
  const { health, error: healthError } = useHealth();
  const { models } = useModels();
  const { history, reply, busy, error, send, reset } = useChat();

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!message.trim() || busy) return;
    await send(message.trim()).catch(() => undefined);
    setMessage("");
  }

  function command(id: string) {
    if (id === "chat") { setActive("Chat"); void reset(); }
    if (id === "clear") setMessage("");
  }

  const currentModel = selectedModel || models[0]?.model || "";
  const toolEvents = normalizeToolEvents(reply?.tool_events ?? []);

  return (
    <main className="shell">
      <Sidebar active={active} onSelect={setActive} />
      <section className="workspace">
        <header>
          <div><span className="eyebrow">DESKTOP AGENT</span><h1>{active === "Chat" ? "What can I do for you?" : active}</h1></div>
          <SystemStatus health={health} error={healthError} />
        </header>
        {active === "Chat" && <>
          <ModelSelector model={currentModel} models={models} onChange={setSelectedModel} />
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}><ChatView history={history} error={error} busy={busy} /></motion.div>
          <ToolActivity events={toolEvents} />
          <form className="composer" onSubmit={submit}>
            <textarea value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Ask SoulOS anything…" disabled={busy} />
            <button disabled={!message.trim() || busy}>{busy ? "Thinking…" : "Send"}</button>
          </form>
        </>}
        {active === "Tools" && <ToolActivity events={toolEvents} />}
        {active === "Memory" && <section className="panel"><div className="panel-title">Memory</div><p>Session memory is managed by the local FastAPI service.</p></section>}
        {active === "Settings" && <Settings apiUrl={apiUrl} />}
      </section>
      <CommandPalette onCommand={command} />
    </main>
  );
}

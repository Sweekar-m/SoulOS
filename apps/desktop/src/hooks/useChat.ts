import { useState } from "react";
import { api } from "../lib/api";
import type { ChatResponse, ConversationMessage } from "../lib/types";

export function useChat() {
  const [sessionId, setSessionId] = useState<string>();
  const [history, setHistory] = useState<ConversationMessage[]>([]);
  const [reply, setReply] = useState<ChatResponse>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  async function send(message: string) {
    if (!message.trim() || busy) return;
    setBusy(true);
    setError(undefined);
    try {
      const result = await api.chat(message.trim(), sessionId);
      setSessionId(result.session_id);
      setReply(result);
      setHistory((current) => [...current,
        { role: "user", content: message.trim(), created_at: new Date().toISOString() },
        { role: "assistant", content: result.response, created_at: new Date().toISOString() },
      ]);
      return result;
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Request failed");
      throw cause;
    } finally {
      setBusy(false);
    }
  }

  function reset() {
    setSessionId(undefined);
    setHistory([]);
    setReply(undefined);
    setError(undefined);
  }

  return { sessionId, history, reply, busy, error, send, reset };
}

import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import type { ChatResponse, ConversationMessage } from "../lib/types";

const SESSION_KEY = "souls.session_id";

export function useChat() {
  const [sessionId, setSessionId] = useState<string>(() => sessionStorage.getItem(SESSION_KEY) ?? "");
  const [history, setHistory] = useState<ConversationMessage[]>([]);
  const [reply, setReply] = useState<ChatResponse>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => {
    if (!sessionId) return;
    void api.conversation(sessionId).then((conversation) => setHistory(conversation.messages)).catch(() => undefined);
  }, [sessionId]);

  const send = useCallback(async (message: string) => {
    if (!message.trim() || busy) return;
    setBusy(true);
    setError(undefined);
    try {
      const result = await api.chat(message.trim(), sessionId || undefined);
      setSessionId(result.session_id);
      sessionStorage.setItem(SESSION_KEY, result.session_id);
      setReply(result);
      const conversation = await api.conversation(result.session_id);
      setHistory(conversation.messages);
      return result;
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Request failed");
      throw cause;
    } finally {
      setBusy(false);
    }
  }, [busy, sessionId]);

  const reset = useCallback(async () => {
    if (sessionId) await api.clearConversation(sessionId).catch(() => undefined);
    sessionStorage.removeItem(SESSION_KEY);
    setSessionId("");
    setHistory([]);
    setReply(undefined);
    setError(undefined);
  }, [sessionId]);

  return { sessionId, history, reply, busy, error, send, reset };
}

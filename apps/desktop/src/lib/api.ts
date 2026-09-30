import type { ChatResponse, Conversation, Health, ModelCatalog } from "./types";

const apiBase = (import.meta.env.VITE_SOULOS_API_URL ?? "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });
  if (!response.ok) throw new Error(`SoulOS API returned ${response.status}`);
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<Health>("/health"),
  models: () => request<ModelCatalog>("/models"),
  chat: (message: string, sessionId?: string) =>
    request<ChatResponse>("/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id: sessionId }),
    }),
  conversation: (sessionId: string) => request<Conversation>(`/conversations/${sessionId}`),
  clearConversation: (sessionId: string) =>
    request<void>(`/conversations/${sessionId}`, { method: "DELETE" }),
};

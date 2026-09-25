import type { ChatResponse, Health } from "./types";

const apiBase = (import.meta.env.VITE_SOULOS_API_URL ?? "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });
  if (!response.ok) throw new Error(`SoulOS API returned ${response.status}`);
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<Health>("/health"),
  chat: (message: string, sessionId?: string) =>
    request<ChatResponse>("/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id: sessionId }),
    }),
};

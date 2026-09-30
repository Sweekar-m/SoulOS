import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import type { Health } from "../lib/types";

export function useHealth(intervalMs = 15000) {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string>();

  const refresh = useCallback(async () => {
    try {
      setHealth(await api.health());
      setError(undefined);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Backend unavailable");
    }
  }, []);

  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => void refresh(), intervalMs);
    return () => window.clearInterval(timer);
  }, [intervalMs, refresh]);

  return { health, error, refresh };
}

import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import type { ModelInfo } from "../lib/types";

export function useModels() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [error, setError] = useState<string>();

  const refresh = useCallback(async () => {
    try {
      const catalog = await api.models();
      setModels(catalog.models);
      setError(undefined);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not load models");
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);
  return { models, error, refresh };
}

export type Health = {
  status: string;
  service: string;
  version: string;
};

export type ChatResponse = {
  session_id: string;
  intent: string;
  confidence: number;
  route: { provider: string; model: string; reason: string; requires_generation: boolean };
  response: string;
  tool_events: Array<Record<string, unknown>>;
};

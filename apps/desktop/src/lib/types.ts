export type Health = {
  status: string;
  service: string;
  version: string;
};

export type ModelInfo = {
  provider: string;
  model: string;
  role: string;
  intent?: string | null;
};

export type ModelCatalog = { models: ModelInfo[] };

export type ChatResponse = {
  session_id: string;
  intent: string;
  confidence: number;
  route: { provider: string; model: string; reason: string; requires_generation: boolean };
  response: string;
  tool_events: Array<Record<string, unknown>>;
};

export type ConversationMessage = {
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
};

export type Conversation = {
  session_id: string;
  messages: ConversationMessage[];
};

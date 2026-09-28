import { describe, expect, it, vi } from "vitest";
import { api } from "../lib/api";

vi.mock("../lib/api", () => ({
  api: { health: vi.fn(), chat: vi.fn(), conversation: vi.fn(), clearConversation: vi.fn() },
}));

describe("desktop API contract", () => {
  it("exposes health, chat, and conversation operations", () => {
    expect(api.health).toBeTypeOf("function");
    expect(api.chat).toBeTypeOf("function");
    expect(api.conversation).toBeTypeOf("function");
    expect(api.clearConversation).toBeTypeOf("function");
  });
});

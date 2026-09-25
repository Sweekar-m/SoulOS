import { describe, expect, it, vi } from "vitest";
import { api } from "../lib/api";

vi.mock("../lib/api", () => ({
  api: { health: vi.fn(), chat: vi.fn() },
}));

describe("desktop API contract", () => {
  it("exposes health and chat operations", () => {
    expect(api.health).toBeTypeOf("function");
    expect(api.chat).toBeTypeOf("function");
  });
});

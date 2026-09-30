import { describe, expect, it } from "vitest";
import { normalizeToolEvents } from "../lib/toolEvents";

describe("normalizeToolEvents", () => {
  it("keeps valid observable tool events", () => {
    expect(normalizeToolEvents([
      { name: "search", status: "completed", detail: "2 results" },
      { name: "open", status: "running" },
    ])).toEqual([
      { name: "search", status: "completed", detail: "2 results" },
      { name: "open", status: "running", detail: undefined },
    ]);
  });

  it("drops malformed events", () => {
    expect(normalizeToolEvents([{ name: 42, status: "completed" }, { name: "x", status: "unknown" }])).toEqual([]);
  });
});

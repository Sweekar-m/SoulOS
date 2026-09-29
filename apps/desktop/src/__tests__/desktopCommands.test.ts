import { describe, expect, it } from "vitest";
import { desktopCommands } from "../lib/desktopCommands";

describe("desktop commands", () => {
  it("exposes stable command ids for the command palette", () => {
    expect(desktopCommands.map((command) => command.id)).toEqual(["chat", "clear"]);
  });

  it("keeps user-facing labels and hints", () => {
    expect(desktopCommands[0]).toMatchObject({ label: "New chat", hint: "Start a fresh conversation" });
    expect(desktopCommands[1]).toMatchObject({ label: "Clear composer", hint: "Focus the input" });
  });
});

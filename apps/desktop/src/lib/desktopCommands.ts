export type DesktopCommand = { id: "chat" | "clear"; label: string; hint: string };

export const desktopCommands: DesktopCommand[] = [
  { id: "chat", label: "New chat", hint: "Start a fresh conversation" },
  { id: "clear", label: "Clear composer", hint: "Focus the input" },
];

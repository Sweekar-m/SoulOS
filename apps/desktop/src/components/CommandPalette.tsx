import { useEffect, useState } from "react";

type Command = { id: string; label: string; hint: string };
const commands: Command[] = [
  { id: "chat", label: "New chat", hint: "Start a fresh conversation" },
  { id: "clear", label: "Clear composer", hint: "Focus the input" },
];

export function CommandPalette({ onCommand }: { onCommand: (id: string) => void }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen((value) => !value);
      }
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  if (!open) return null;
  const filtered = commands.filter((command) => command.label.toLowerCase().includes(query.toLowerCase()));
  return (
    <div className="palette-backdrop" onClick={() => setOpen(false)}>
      <section className="command-palette" onClick={(event) => event.stopPropagation()} role="dialog" aria-label="Command palette">
        <input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search commands…" />
        {filtered.map((command) => (
          <button key={command.id} onClick={() => { onCommand(command.id); setOpen(false); }}>
            <strong>{command.label}</strong><small>{command.hint}</small>
          </button>
        ))}
      </section>
    </div>
  );
}

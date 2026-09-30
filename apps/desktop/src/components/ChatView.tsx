import type { ConversationMessage } from "../lib/types";

type ChatViewProps = {
  history: ConversationMessage[];
  error?: string;
  busy?: boolean;
};

export function ChatView({ history, error, busy }: ChatViewProps) {
  return (
    <section className="conversation" aria-live="polite" aria-busy={busy}>
      {history.length ? history.map((item, index) => (
        <article key={`${item.created_at}-${index}`} className={item.role === "user" ? "user" : "assistant"}>
          <div className="meta">{item.role}</div>
          <p>{item.content}</p>
        </article>
      )) : (
        <p className="empty">Local orchestration is ready. Commands are classified before tools or models are selected.</p>
      )}
      {busy && <p className="meta">SoulOS is thinking…</p>}
      {error && <small className="error" role="alert">{error}</small>}
    </section>
  );
}

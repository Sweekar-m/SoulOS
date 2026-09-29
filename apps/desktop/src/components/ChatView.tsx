import type { ConversationMessage } from "../lib/types";

export function ChatView({ history }: { history: ConversationMessage[] }) {
  return (
    <section className="conversation" aria-live="polite">
      {history.length ? history.map((item, index) => (
        <article key={`${item.created_at}-${index}`} className={item.role === "user" ? "user" : "assistant"}>
          <div className="meta">{item.role}</div>
          <p>{item.content}</p>
        </article>
      )) : (
        <p className="empty">Local orchestration is ready. Commands are classified before tools or models are selected.</p>
      )}
    </section>
  );
}

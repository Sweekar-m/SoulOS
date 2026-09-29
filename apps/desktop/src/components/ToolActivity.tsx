export type ToolActivityEvent = {
  name: string;
  status: "running" | "completed" | "failed";
  detail?: string;
};

export function ToolActivity({ events }: { events: ToolActivityEvent[] }) {
  if (!events.length) return null;
  return (
    <section className="tool-activity" aria-label="Tool activity">
      <div className="panel-title">Activity</div>
      {events.map((event, index) => (
        <div className="activity-row" key={`${event.name}-${index}`}>
          <span>{event.name}</span>
          <span className={`activity-status ${event.status}`}>{event.status}</span>
          {event.detail && <small>{event.detail}</small>}
        </div>
      ))}
    </section>
  );
}

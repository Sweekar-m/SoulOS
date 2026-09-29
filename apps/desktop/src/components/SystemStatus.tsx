import type { Health } from "../lib/types";

type Props = { health: Health | null };

export function SystemStatus({ health }: Props) {
  return (
    <div className="system-status" role="status">
      <span className={`status-dot ${health ? "online" : "offline"}`} />
      <span>{health ? "Backend online" : "Connecting to backend"}</span>
    </div>
  );
}

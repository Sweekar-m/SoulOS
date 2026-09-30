import type { Health } from "../lib/types";

type Props = { health: Health | null; error?: string };

export function SystemStatus({ health, error }: Props) {
  const online = Boolean(health) && !error;
  return (
    <div className="system-status" role="status" title={error ?? health?.version}>
      <span className={`status-dot ${online ? "online" : "offline"}`} />
      <span>{online ? "Backend online" : error ? "Backend unavailable" : "Connecting to backend"}</span>
    </div>
  );
}

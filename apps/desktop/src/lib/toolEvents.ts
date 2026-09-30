import type { ToolActivityEvent } from "../components/ToolActivity";

export function normalizeToolEvents(events: Array<Record<string, unknown>>): ToolActivityEvent[] {
  return events.flatMap((event) => {
    const name = event.name;
    const status = event.status;
    if (typeof name !== "string" || (status !== "running" && status !== "completed" && status !== "failed")) return [];
    return [{ name, status, detail: typeof event.detail === "string" ? event.detail : undefined }];
  });
}

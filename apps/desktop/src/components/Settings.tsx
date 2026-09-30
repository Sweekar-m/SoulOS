type Props = { apiUrl: string };

export function Settings({ apiUrl }: Props) {
  return (
    <section className="settings-panel">
      <div className="panel-title">Desktop settings</div>
      <label>
        <span>Local API URL</span>
        <input value={apiUrl} readOnly aria-label="Local API URL" />
      </label>
      <small>Set VITE_SOULOS_API_URL before starting the desktop app. Credentials remain outside the UI.</small>
    </section>
  );
}

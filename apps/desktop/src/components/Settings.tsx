type Props = {
  apiUrl: string;
  onApiUrlChange: (value: string) => void;
};

export function Settings({ apiUrl, onApiUrlChange }: Props) {
  return (
    <section className="settings-panel">
      <div className="panel-title">Desktop settings</div>
      <label>
        <span>Local API URL</span>
        <input value={apiUrl} onChange={(event) => onApiUrlChange(event.target.value)} />
      </label>
      <small>Stored locally in this session. Credentials remain outside the UI.</small>
    </section>
  );
}

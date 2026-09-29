type Props = {
  model: string;
  models: string[];
  onChange: (model: string) => void;
};

export function ModelSelector({ model, models, onChange }: Props) {
  return (
    <label className="model-selector">
      <span>Model</span>
      <select value={model} onChange={(event) => onChange(event.target.value)}>
        {models.map((name) => <option key={name} value={name}>{name}</option>)}
      </select>
    </label>
  );
}

import type { ModelInfo } from "../lib/types";

type Props = {
  model: string;
  models: ModelInfo[];
  onChange: (model: string) => void;
};

export function ModelSelector({ model, models, onChange }: Props) {
  return (
    <label className="model-selector">
      <span>Model</span>
      <select value={model} onChange={(event) => onChange(event.target.value)} disabled={!models.length}>
        {!models.length && <option value="">No models configured</option>}
        {models.map((item) => <option key={`${item.provider}:${item.model}`} value={item.model}>{item.model}</option>)}
      </select>
    </label>
  );
}

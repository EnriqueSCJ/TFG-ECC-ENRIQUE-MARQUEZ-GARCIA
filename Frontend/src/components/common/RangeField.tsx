interface RangeFieldProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
}

export function RangeField({ label, value, onChange, min, max, step = 1 }: RangeFieldProps) {
  return (
    <label className="grid gap-2 text-sm text-slate-700">
      <span className="flex items-center justify-between gap-3">
        <span className="font-medium text-slate-800">{label}</span>
        <span className="rounded border border-slate-200 bg-white px-2 py-1 font-mono text-xs text-slate-700">
          {value}
        </span>
      </span>
      <input
        type="range"
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={(event) => onChange(Number(event.target.value))}
        className="h-2 cursor-pointer accent-indigo-700"
      />
    </label>
  );
}

import { useEffect, useId, useState } from "react";
import { cn } from "../../lib/styles";

const DEFAULT_PRIME_OPTIONS = [17, 19, 23, 29, 43, 97, 233, 997];

interface PrimeFieldProps {
  label?: string;
  value: number | null;
  onChange: (value: number) => void;
  allowEmpty?: boolean;
  min?: number;
  max?: number;
  onEmpty?: () => void;
  options?: number[];
  className?: string;
}

export function PrimeField({
  label = "Primo p",
  value,
  onChange,
  allowEmpty = false,
  min = 5,
  max = 997,
  onEmpty,
  options = DEFAULT_PRIME_OPTIONS,
  className,
}: PrimeFieldProps) {
  const datalistId = useId();
  const [textValue, setTextValue] = useState(value === null ? "" : String(value));

  useEffect(() => {
    setTextValue(value === null ? "" : String(value));
  }, [value]);

  const commitValue = (rawValue: string) => {
    const nextValue = Number(rawValue);
    if (Number.isFinite(nextValue) && nextValue >= min) {
      onChange(nextValue);
    }
  };

  return (
    <label className={cn("grid gap-1.5 text-sm text-slate-700", className)}>
      <span className="font-medium text-slate-800">{label}</span>
      <input
        type="number"
        list={datalistId}
        min={min}
        max={max}
        step={1}
        value={textValue}
        onChange={(event) => {
          const rawValue = event.target.value;
          setTextValue(rawValue);

          if (allowEmpty && rawValue === "") {
            onEmpty?.();
            return;
          }

          if (rawValue !== "") {
            commitValue(rawValue);
          }
        }}
        onBlur={() => {
          if (textValue === "" || !Number.isFinite(Number(textValue)) || Number(textValue) < min) {
            setTextValue(value === null ? "" : String(value));
          }
        }}
        className="h-10 rounded-md border border-slate-300 bg-white px-3 font-mono text-sm text-slate-900 outline-none transition focus:border-indigo-700 focus:ring-2 focus:ring-indigo-100"
      />
      <datalist id={datalistId}>
        {options.map((prime) => (
          <option key={prime} value={prime} />
        ))}
      </datalist>
    </label>
  );
}

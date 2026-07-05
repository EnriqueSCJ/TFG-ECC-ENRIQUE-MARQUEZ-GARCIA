import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { cn } from "../../lib/styles";

interface NumericFieldProps {
  label: ReactNode;
  value: number | null;
  onChange: (value: number) => void;
  allowEmpty?: boolean;
  min?: number;
  max?: number;
  onEmpty?: () => void;
  step?: number;
  className?: string;
}

export function NumericField({
  label,
  value,
  onChange,
  allowEmpty = false,
  min,
  max,
  onEmpty,
  step = 1,
  className,
}: NumericFieldProps) {
  const [textValue, setTextValue] = useState(value === null ? "" : String(value));

  useEffect(() => {
    setTextValue(value === null ? "" : String(value));
  }, [value]);

  return (
    <label className={cn("grid min-w-0 gap-1.5 text-sm text-slate-700", className)}>
      <span className="font-medium text-slate-800">{label}</span>
      <input
        type="number"
        value={textValue}
        min={min}
        max={max}
        step={step}
        onChange={(event) => {
          const rawValue = event.target.value;
          setTextValue(rawValue);

          if (allowEmpty && rawValue === "") {
            onEmpty?.();
            return;
          }

          const nextValue = Number(rawValue);
          if (Number.isFinite(nextValue)) {
            onChange(nextValue);
          }
        }}
        className="h-10 w-full min-w-0 rounded-md border border-slate-300 bg-white px-3 font-mono text-sm text-slate-900 outline-none transition focus:border-indigo-700 focus:ring-2 focus:ring-indigo-100"
      />
    </label>
  );
}

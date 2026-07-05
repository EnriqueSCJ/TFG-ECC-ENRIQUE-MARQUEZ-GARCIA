import { cn } from "../../lib/styles";

interface SegmentedOption<T extends string> {
  value: T;
  label: string;
}

interface SegmentedControlProps<T extends string> {
  value: T;
  options: Array<SegmentedOption<T>>;
  onChange: (value: T) => void;
}

export function SegmentedControl<T extends string>({
  value,
  options,
  onChange,
}: SegmentedControlProps<T>) {
  return (
    <div className="inline-flex rounded-lg border border-slate-300 bg-slate-100 p-1">
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => onChange(option.value)}
          className={cn(
            "rounded-md px-3 py-1.5 text-sm font-medium transition",
            value === option.value
              ? "bg-white text-indigo-900 shadow-sm"
              : "text-slate-600 hover:bg-white/70 hover:text-slate-950",
          )}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

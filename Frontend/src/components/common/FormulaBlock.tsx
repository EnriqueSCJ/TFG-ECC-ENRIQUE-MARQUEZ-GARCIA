import { BlockMath } from "react-katex";

interface FormulaBlockProps {
  math: string;
  compact?: boolean;
}

export function FormulaBlock({ math, compact = false }: FormulaBlockProps) {
  return (
    <div
      className={
        compact
          ? "rounded-md bg-slate-50 px-3 py-2 text-slate-900"
          : "rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900"
      }
    >
      <BlockMath math={math} />
    </div>
  );
}

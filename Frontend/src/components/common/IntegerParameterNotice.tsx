import { CircleDotDashed } from "lucide-react";
import { InlineMath } from "react-katex";
import { formatNumber } from "../../lib/eccMath";

interface IntegerParameterNoticeProps {
  a: number;
  b: number;
  onRound: () => void;
}

export function IntegerParameterNotice({ a, b, onRound }: IntegerParameterNoticeProps) {
  return (
    <div className="grid gap-3 rounded-md border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-950">
      <div className="flex min-w-0 items-start gap-3">
        <CircleDotDashed className="mt-0.5 h-4 w-4 shrink-0 text-amber-700" aria-hidden="true" />
        <div className="min-w-0">
          <p className="font-semibold">
            Para trabajar en el cuerpo finito <InlineMath math="\mathbb{F}_p" />, los coeficientes deben ser enteros
          </p>
          <p className="mt-1 text-amber-800">
            Valores actuales:
            <span className="mt-0.5 block whitespace-nowrap font-mono">
              a = {formatNumber(a)}, b = {formatNumber(b)}.
            </span>
          </p>
        </div>
      </div>
      <button
        type="button"
        onClick={onRound}
        className="inline-flex h-9 justify-self-start items-center justify-center rounded-md border border-amber-300 bg-white px-3 text-sm font-medium text-amber-900 transition hover:bg-amber-100"
      >
        Aproximar a enteros
      </button>
    </div>
  );
}

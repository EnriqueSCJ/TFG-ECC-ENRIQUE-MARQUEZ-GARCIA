import { useDeferredValue, useMemo } from "react";
import { ConceptHint } from "../components/common/ConceptHint";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { PrimeField } from "../components/common/PrimeField";
import { RangeField } from "../components/common/RangeField";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { PlotSurface } from "../components/visualization/PlotSurface";
import {
  buildContinuousCurve,
  formatNumber,
  realDiscriminant,
} from "../lib/eccMath";
import { useBackendData } from "../hooks/useBackendData";
import { useDebouncedValue } from "../hooks/useDebouncedValue";
import { eccService } from "../services/eccService";
import { useCurveStore } from "../store/curveStore";

function canComputeFiniteDelta(a: number, b: number, p: number): boolean {
  return Number.isInteger(a) && Number.isInteger(b) && Number.isInteger(p) && p > 3;
}

const INITIAL_X_RANGE: [number, number] = [-4.5, 4.5];
const INITIAL_Y_RANGE: [number, number] = [-6, 6];
const CURVE_RENDER_X_RANGE: [number, number] = [-36, 36];
const PAN_BOUNDS = {
  x: CURVE_RENDER_X_RANGE,
};
const discriminantHint = (
  <ConceptHint
    title="Discriminante"
    description="Para una curva y² = x³ + ax + b, el discriminante detecta singularidades. Si Δ = 0, la curva tiene una cúspide o un nodo y deja de definir una curva elíptica no singular."
  >
    Δ
  </ConceptHint>
);

export function WeierstrassExplorer() {
  const parameters = useCurveStore((state) => state.parameters);
  const setParameters = useCurveStore((state) => state.setParameters);
  const plotParameters = useDeferredValue(parameters);
  const validationParameters = useDebouncedValue(parameters, 180);
  const setPrime = (p: number) =>
    setParameters({ p: Math.max(5, Math.min(997, Math.trunc(p))) });

  const continuousCurve = useMemo(
    () =>
      buildContinuousCurve(
        plotParameters.a,
        plotParameters.b,
        CURVE_RENDER_X_RANGE[0],
        CURVE_RENDER_X_RANGE[1],
        3000,
      ),
    [plotParameters.a, plotParameters.b],
  );
  const deltaReal = realDiscriminant(parameters.a, parameters.b);
  const canComputeFinite = canComputeFiniteDelta(
    validationParameters.a,
    validationParameters.b,
    validationParameters.p,
  );
  const finiteValidation = useBackendData(
    () => eccService.validateCurve(validationParameters),
    [validationParameters],
    canComputeFinite,
  );
  const deltaFinite = canComputeFinite ? finiteValidation.data?.discriminant ?? null : null;
  const isSingularReal = Math.abs(deltaReal) < 0.001;

  const data = useMemo(
    () => [
      {
        x: continuousCurve.x,
        y: continuousCurve.upper,
        type: "scatter",
        mode: "lines",
        name: "y > 0",
        connectgaps: false,
        hovertemplate: "x=%{x:.2f}<br>y=%{y:.2f}<extra>Rama superior</extra>",
        line: { color: "#2563eb", width: 2.5 },
      },
      {
        x: continuousCurve.x,
        y: continuousCurve.lower,
        type: "scatter",
        mode: "lines",
        name: "y < 0",
        connectgaps: false,
        hovertemplate: "x=%{x:.2f}<br>y=%{y:.2f}<extra>Rama inferior</extra>",
        line: { color: "#b45309", width: 2.5 },
      },
    ],
    [continuousCurve],
  );
  const plotLayout = useMemo<Record<string, unknown>>(
    () => ({
      xaxis: { range: INITIAL_X_RANGE, title: "x" },
      yaxis: { range: INITIAL_Y_RANGE, title: "y", scaleanchor: "x", scaleratio: 1 },
    }),
    [],
  );

  return (
    <div className="grid gap-5 xl:grid-cols-[22rem_1fr]">
      <ScientificPanel
        title="Parámetros reales"
        description="Forma corta de Weierstrass sobre los reales."
      >
        <div className="grid gap-5">
          <FormulaBlock
            math={`E: y^2=x^3+(${formatNumber(parameters.a)})x+(${formatNumber(parameters.b)})`}
          />

          <RangeField
            label="Parámetro a"
            min={-5}
            max={5}
            step={0.1}
            value={parameters.a}
            onChange={(a) => setParameters({ a })}
          />
          <RangeField
            label="Parámetro b"
            min={-5}
            max={5}
            step={0.1}
            value={parameters.b}
            onChange={(b) => setParameters({ b })}
          />
          <PrimeField value={parameters.p} onChange={setPrime} />

          <div className="grid gap-3 border-t border-slate-200 pt-4 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-slate-600">{discriminantHint} real</span>
              <span className="font-mono text-slate-900">{formatNumber(deltaReal, 4)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-600">Estado</span>
              <span className={isSingularReal ? "text-rose-700" : "text-emerald-700"}>
                {isSingularReal ? "Singular" : "No singular"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-600">{"\u0394 (mod p)"}</span>
              <span className="font-mono text-slate-900">
                {deltaFinite === null ? "No definido" : deltaFinite}
              </span>
            </div>
          </div>

          <FormulaBlock math="\Delta=-16(4a^3+27b^2)" compact />
        </div>
      </ScientificPanel>

      <ScientificPanel title="Curva continua 2D" description="Renderizado numérico de ramas reales.">
        <PlotSurface
          data={data}
          height={520}
          layout={plotLayout}
          maxZoomOutSteps={3}
          panBounds={PAN_BOUNDS}
          fitPanYToVisibleData
        />
      </ScientificPanel>
    </div>
  );
}

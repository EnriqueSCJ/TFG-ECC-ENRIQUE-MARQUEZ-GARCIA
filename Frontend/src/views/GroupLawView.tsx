import { useMemo, useState } from "react";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { RealPointSelector } from "../components/common/PointControls";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { SegmentedControl } from "../components/common/SegmentedControl";
import { PlotSurface } from "../components/visualization/PlotSurface";
import {
  buildContinuousCurve,
  formatNumber,
  formatPoint,
  realGroupOperation,
} from "../lib/eccMath";
import { useCurveStore } from "../store/curveStore";
import { GroupOperationResult, isPointAtInfinity } from "../types/ecc";

type GroupMode = "add" | "double";

const INITIAL_X_RANGE: [number, number] = [-4.5, 4.5];
const INITIAL_Y_RANGE: [number, number] = [-6, 6];
const CURVE_RENDER_X_RANGE: [number, number] = [-36, 36];
const PAN_BOUNDS = {
  x: CURVE_RENDER_X_RANGE,
};

export function GroupLawView() {
  const [mode, setMode] = useState<GroupMode>("add");
  const parameters = useCurveStore((state) => state.parameters);
  const pointP = useCurveStore((state) => state.pointP);
  const pointQ = useCurveStore((state) => state.pointQ);
  const setPointP = useCurveStore((state) => state.setPointP);
  const setPointQ = useCurveStore((state) => state.setPointQ);

  const continuousCurve = useMemo(
    () =>
      buildContinuousCurve(
        parameters.a,
        parameters.b,
        CURVE_RENDER_X_RANGE[0],
        CURVE_RENDER_X_RANGE[1],
        3000,
      ),
    [parameters.a, parameters.b],
  );

  const operation = useMemo<{ value: GroupOperationResult | null; error: string | null }>(() => {
    try {
      return {
        value: realGroupOperation(pointP, pointQ, parameters, mode, CURVE_RENDER_X_RANGE),
        error: null,
      };
    } catch (error) {
      return {
        value: null,
        error: error instanceof Error ? error.message : "No se pudo calcular la ley de grupo.",
      };
    }
  }, [mode, parameters, pointP, pointQ]);

  const activeQ = mode === "double" ? pointP : pointQ;
  const operationNote = useMemo(() => {
    if (!operation.value) return null;

    if (isPointAtInfinity(operation.value.result)) {
      return "El resultado es 𝒪: la recta es vertical y el tercer corte está en el punto del infinito.";
    }

    return null;
  }, [operation.value]);

  const data = useMemo(() => {
    const traces: Array<Record<string, unknown>> = [
      {
        x: continuousCurve.x,
        y: continuousCurve.upper,
        type: "scatter",
        mode: "lines",
        name: "E, y > 0",
        connectgaps: false,
        hovertemplate: "x=%{x:.2f}<br>y=%{y:.2f}<extra>Rama superior</extra>",
        line: { color: "#2563eb", width: 2.5 },
      },
      {
        x: continuousCurve.x,
        y: continuousCurve.lower,
        type: "scatter",
        mode: "lines",
        name: "E, y < 0",
        connectgaps: false,
        hovertemplate: "x=%{x:.2f}<br>y=%{y:.2f}<extra>Rama inferior</extra>",
        line: { color: "#b45309", width: 2.5 },
      },
      {
        x: [pointP.x, activeQ.x],
        y: [pointP.y, activeQ.y],
        type: "scatter",
        mode: "markers+text",
        name: mode === "double" ? "P" : "P, Q",
        text: mode === "double" ? ["P", "P"] : ["P", "Q"],
        textposition: "top center",
        hovertemplate: "%{text}: (%{x:.2f}, %{y:.2f})<extra></extra>",
        marker: {
          color: mode === "double" ? ["#111827", "#111827"] : ["#111827", "#7c2d12"],
          size: 11,
          line: { color: "#ffffff", width: 2 },
        },
      },
    ];

    if (operation.value?.line) {
      traces.push({
        x: operation.value.line.x,
        y: operation.value.line.y,
        type: "scatter",
        mode: "lines",
        name: mode === "double" ? "tangente" : "cuerda",
        hoverinfo: "skip",
        line: { color: "#4f46e5", width: 2, dash: "dash" },
      });
    }

    if (operation.value?.reflectedPoint) {
      traces.push({
        x: [operation.value.reflectedPoint.x, operation.value.result.x],
        y: [operation.value.reflectedPoint.y, operation.value.result.y],
        type: "scatter",
        mode: "markers+lines+text",
        name: "resultado",
        text: ["-R", mode === "double" ? "2P" : "P+Q"],
        textposition: "right center",
        hovertemplate: "%{text}: (%{x:.2f}, %{y:.2f})<extra></extra>",
        marker: { color: ["#4f46e5", "#047857"], size: 12, line: { color: "#ffffff", width: 2 } },
        line: { color: "#64748b", width: 1.5, dash: "dot" },
      });
    }

    return traces;
  }, [activeQ, continuousCurve, mode, operation.value, pointP]);

  return (
    <div className="grid gap-5 xl:grid-cols-[24rem_1fr]">
      <ScientificPanel
        title="Cuerda y tangente"
        description="Operación geométrica sobre la curva real seleccionada."
        action={
          <SegmentedControl
            value={mode}
            onChange={setMode}
            options={[
              { value: "add", label: "P + Q" },
              { value: "double", label: "P + P" },
            ]}
          />
        }
      >
        <div className="grid gap-4">
          <FormulaBlock math="y^2=x^3+ax+b" />

          <div className="grid gap-3">
            <RealPointSelector
              label="P"
              value={pointP}
              parameters={parameters}
              onChange={setPointP}
            />
            {mode === "add" ? (
              <RealPointSelector
                label="Q"
                value={pointQ}
                parameters={parameters}
                onChange={setPointQ}
              />
            ) : null}
          </div>

          {operation.error ? <ErrorBanner message={operation.error} /> : null}

          {operation.value ? (
            <div className="grid gap-3 border-t border-slate-200 pt-4 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-slate-600">Resultado</span>
                <span className="font-mono text-emerald-700">{formatPoint(operation.value.result)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-600">{"\u03bb"}</span>
                <span className="font-mono text-slate-900">
                  {operation.value.slope === undefined
                    ? "No definida"
                    : formatNumber(operation.value.slope)}
                </span>
              </div>
              {operationNote ? (
                <div className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-amber-900">
                  {operationNote}
                </div>
              ) : null}
              {operation.value.steps.map((step) => (
                <div key={step.title} className="border-t border-slate-200 pt-3">
                  <p className="font-medium text-slate-900">{step.title}</p>
                  <p className="mt-1 text-slate-600">{step.description}</p>
                </div>
              ))}
            </div>
          ) : null}
        </div>
      </ScientificPanel>

      <ScientificPanel title="Visualización de la operación">
        <PlotSurface
          data={data}
          height={560}
          layout={{
            xaxis: { range: INITIAL_X_RANGE, title: "x" },
            yaxis: { range: INITIAL_Y_RANGE, title: "y", scaleanchor: "x", scaleratio: 1 },
          }}
          maxZoomOutSteps={3}
          panBounds={PAN_BOUNDS}
          fitPanYToVisibleData
        />
      </ScientificPanel>
    </div>
  );
}

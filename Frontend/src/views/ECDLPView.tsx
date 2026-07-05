import { Pause, Play, RotateCcw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { IntegerParameterNotice } from "../components/common/IntegerParameterNotice";
import { NumericField } from "../components/common/NumericField";
import { FinitePointSelect } from "../components/common/PointControls";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { PlotSurface } from "../components/visualization/PlotSurface";
import { useBackendData } from "../hooks/useBackendData";
import { formatPoint } from "../lib/eccMath";
import { hasIntegerCurveCoefficients, roundCurveCoefficients } from "../lib/finiteParameters";
import {
  finiteAxisStep,
  finiteBackgroundMarkerSize,
  shouldUseDetailedFiniteHover,
} from "../lib/finitePlot";
import { eccService } from "../services/eccService";
import { useCurveStore } from "../store/curveStore";

export function ECDLPView() {
  const [visibleStep, setVisibleStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const parameters = useCurveStore((state) => state.parameters);
  const pointP = useCurveStore((state) => state.pointP);
  const setPointP = useCurveStore((state) => state.setPointP);
  const scalarK = useCurveStore((state) => state.scalarK);
  const setScalarK = useCurveStore((state) => state.setScalarK);
  const setParameters = useCurveStore((state) => state.setParameters);
  const hasIntegerCoefficients = hasIntegerCurveCoefficients(parameters);

  const finiteData = useBackendData(
    () => eccService.getFinitePoints(parameters),
    [hasIntegerCoefficients, parameters],
    hasIntegerCoefficients,
  );
  const points = finiteData.data?.points ?? [];
  const axisStep = finiteAxisStep(parameters.p);
  const baseMarkerSize = finiteBackgroundMarkerSize(parameters.p);
  const detailedHover = shouldUseDetailedFiniteHover(parameters.p);

  const computation = useBackendData(
    () => eccService.multiplyPoint(parameters, pointP, scalarK),
    [hasIntegerCoefficients, parameters, pointP, scalarK],
    hasIntegerCoefficients,
  );

  useEffect(() => {
    setVisibleStep(0);
    setIsPlaying(false);
  }, [parameters, pointP, scalarK]);

  useEffect(() => {
    if (!isPlaying || !computation.data || computation.data.walk.length === 0) return;

    const interval = window.setInterval(() => {
      setVisibleStep((current) => {
        if (current >= computation.data!.walk.length - 1) {
          window.clearInterval(interval);
          setIsPlaying(false);
          return current;
        }
        return current + 1;
      });
    }, 650);

    return () => window.clearInterval(interval);
  }, [computation.data, isPlaying]);

  const walk = computation.data?.walk ?? [];
  const visibleWalk = walk.slice(0, visibleStep + 1);
  const currentPoint = visibleWalk.at(-1)?.point;

  const data = useMemo(
    () => [
      {
        x: points.map((point) => point.x),
        y: points.map((point) => point.y),
        type: "scatter",
        mode: "markers",
        name: "E(𝔽ₚ)",
        text: detailedHover ? points.map((point) => `(${point.x}, ${point.y})`) : undefined,
        hovertemplate: detailedHover
          ? "%{text}<extra>E(𝔽ₚ)</extra>"
          : "x=%{x}<br>y=%{y}<extra>E(𝔽ₚ)</extra>",
        marker: {
          color: "rgba(100, 116, 139, 0.34)",
          size: baseMarkerSize,
          line: { color: "#ffffff", width: detailedHover ? 1 : 0 },
        },
      },
      {
        x: visibleWalk.map((step) => step.point.x),
        y: visibleWalk.map((step) => step.point.y),
        type: "scatter",
        mode: "lines+markers",
        name: "recorrido",
        text: visibleWalk.map((step) =>
          step.point.x === null ? "𝒪" : `${step.index}P = ${formatPoint(step.point)}`,
        ),
        hovertemplate: "%{text}<extra></extra>",
        line: { color: "#2563eb", width: 2 },
        marker: { color: "#2563eb", size: 9, line: { color: "#ffffff", width: 1.5 } },
      },
      {
        x: currentPoint && currentPoint.x !== null ? [currentPoint.x] : [],
        y: currentPoint && currentPoint.y !== null ? [currentPoint.y] : [],
        type: "scatter",
        mode: "markers+text",
        name: "actual",
        text: currentPoint && currentPoint.x !== null ? [`${visibleStep}P`] : [],
        textposition: "top center",
        hovertemplate: "%{text}: (%{x}, %{y})<extra>paso actual</extra>",
        marker: { color: "#b45309", size: 15, symbol: "circle-open", line: { width: 3 } },
      },
    ],
    [baseMarkerSize, currentPoint, detailedHover, points, visibleWalk],
  );

  return (
    <div className="grid gap-5 xl:grid-cols-[24rem_1fr]">
      <ScientificPanel
        title="Multiplicación escalar"
        description="Q = kP como recorrido discreto sobre el grupo E(𝔽ₚ)."
      >
        <div className="grid gap-4">
          <FormulaBlock math="Q=kP=P+\cdots+P" />

          <div className="grid gap-3 sm:grid-cols-[8rem_1fr]">
            <NumericField label="k" min={0} max={80} value={scalarK} onChange={setScalarK} />
            <FinitePointSelect
              label="P base"
              value={pointP}
              points={points}
              onChange={setPointP}
            />
          </div>

          {!hasIntegerCoefficients ? (
            <IntegerParameterNotice
              a={parameters.a}
              b={parameters.b}
              onRound={() => setParameters(roundCurveCoefficients(parameters))}
            />
          ) : null}
          {finiteData.error ? <ErrorBanner message={finiteData.error} /> : null}
          {computation.error ? <ErrorBanner message={computation.error} /> : null}

          <div className="flex flex-wrap gap-2 border-t border-slate-200 pt-4">
            <button
              type="button"
              onClick={() => setIsPlaying((value) => !value)}
              className="inline-flex h-10 items-center gap-2 rounded-md bg-indigo-700 px-3 text-sm font-medium text-white transition hover:bg-indigo-600"
              title={isPlaying ? "Pausar" : "Reproducir"}
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              {isPlaying ? "Pausar" : "Reproducir"}
            </button>
            <button
              type="button"
              onClick={() => {
                setVisibleStep(0);
                setIsPlaying(false);
              }}
              className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              title="Reiniciar"
            >
              <RotateCcw className="h-4 w-4" />
              Reiniciar
            </button>
          </div>

          <div className="grid gap-3 border-t border-slate-200 pt-4 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-slate-600">Q</span>
              <span className="font-mono text-emerald-700">
                {computation.loading
                  ? "..."
                  : computation.data
                    ? formatPoint(computation.data.result)
                    : "n/a"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-600">Paso visible</span>
              <span className="font-mono text-slate-900">
                {visibleStep}/{Math.max(walk.length - 1, 0)}
              </span>
            </div>
          </div>
        </div>
      </ScientificPanel>

      <ScientificPanel title="Animación de saltos">
        <PlotSurface
          data={data}
          height={560}
          layout={{
            xaxis: {
              range: [-0.8, parameters.p - 0.2],
              dtick: axisStep,
              tick0: 0,
              title: "x",
            },
            yaxis: {
              range: [-0.8, parameters.p - 0.2],
              dtick: axisStep,
              tick0: 0,
              title: "y",
              scaleanchor: "x",
            },
          }}
        />
      </ScientificPanel>
    </div>
  );
}

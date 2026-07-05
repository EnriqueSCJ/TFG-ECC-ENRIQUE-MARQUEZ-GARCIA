import { useMemo, useState } from "react";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { IntegerParameterNotice } from "../components/common/IntegerParameterNotice";
import { NumericField } from "../components/common/NumericField";
import { PrimeField } from "../components/common/PrimeField";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { PlotSurface } from "../components/visualization/PlotSurface";
import { useBackendData } from "../hooks/useBackendData";
import { hasIntegerCurveCoefficients, roundCurveCoefficients } from "../lib/finiteParameters";
import { finiteAxisStep, finiteMarkerSize } from "../lib/finitePlot";
import { eccService } from "../services/eccService";
import { useCurveStore } from "../store/curveStore";

type DraftFiniteParameters = {
  a: number | null;
  b: number | null;
  p: number | null;
};

export function FiniteFieldView() {
  const parameters = useCurveStore((state) => state.parameters);
  const setParameters = useCurveStore((state) => state.setParameters);
  const [draftParameters, setDraftParameters] = useState<DraftFiniteParameters>(() => ({
    a: parameters.a,
    b: parameters.b,
    p: parameters.p,
  }));

  const finiteParameters = useMemo(() => {
    if (
      draftParameters.a === null ||
      draftParameters.b === null ||
      draftParameters.p === null
    ) {
      return null;
    }

    return {
      ...parameters,
      a: draftParameters.a,
      b: draftParameters.b,
      p: draftParameters.p,
    };
  }, [draftParameters, parameters]);
  const hasIntegerCoefficients =
    finiteParameters === null || hasIntegerCurveCoefficients(finiteParameters);
  const canRequestFiniteData = finiteParameters !== null && hasIntegerCoefficients;

  const finiteData = useBackendData(
    () => eccService.getFinitePoints(finiteParameters!),
    [finiteParameters],
    canRequestFiniteData,
  );
  const validationError = finiteData.error;
  const points = finiteData.data?.points ?? [];
  const delta = finiteData.data?.discriminant ?? null;
  const plotPrime = finiteParameters?.p ?? parameters.p;
  const axisStep = finiteAxisStep(plotPrime);
  const markerSize = finiteMarkerSize(plotPrime);
  const shouldRenderPlot = canRequestFiniteData && !validationError && points.length > 0;

  function updateDraftParameter(field: keyof DraftFiniteParameters, value: number | null) {
    setDraftParameters((current) => ({ ...current, [field]: value }));

    if (value !== null) {
      setParameters({ [field]: value });
    }
  }

  function roundDraftCoefficients() {
    if (draftParameters.a === null || draftParameters.b === null) return;

    const rounded = roundCurveCoefficients({
      a: draftParameters.a,
      b: draftParameters.b,
    });

    setDraftParameters((current) => ({ ...current, ...rounded }));
    setParameters(rounded);
  }

  const data = useMemo(() => {
    if (!shouldRenderPlot || !finiteParameters) return [];

    return [
      {
        x: points.map((point) => point.x),
        y: points.map((point) => point.y),
        type: "scatter",
        mode: "markers",
        name: "E(𝔽ₚ)",
        text: points.map((point) => `(${point.x}, ${point.y})`),
        hovertemplate: "%{text}<extra>punto válido</extra>",
        marker: { color: "#2563eb", size: markerSize, line: { color: "#ffffff", width: 1.5 } },
      },
      {
        x: [0, Math.max(finiteParameters.p - 1, 1)],
        y: [finiteParameters.p / 2, finiteParameters.p / 2],
        type: "scatter",
        mode: "lines",
        name: "y = p/2",
        hoverinfo: "skip",
        line: { color: "#94a3b8", dash: "dot", width: 1.5 },
      },
    ];
  }, [finiteParameters, markerSize, points, shouldRenderPlot]);

  return (
    <div className="grid gap-5 xl:grid-cols-[24rem_1fr]">
      <ScientificPanel
        title="Dominio finito"
        description="Curva reducida en el cuerpo primo 𝔽ₚ."
      >
        <div className="grid gap-4">
          <FormulaBlock math="E(\mathbb{F}_p): y^2 \equiv x^3+ax+b \pmod{p}" />

          <div className="grid grid-cols-3 gap-3">
            <NumericField
              allowEmpty
              label="a"
              value={draftParameters.a}
              onChange={(a) => updateDraftParameter("a", a)}
              onEmpty={() => updateDraftParameter("a", null)}
            />
            <NumericField
              allowEmpty
              label="b"
              value={draftParameters.b}
              onChange={(b) => updateDraftParameter("b", b)}
              onEmpty={() => updateDraftParameter("b", null)}
            />
            <PrimeField
              allowEmpty
              label="p"
              value={draftParameters.p}
              onChange={(p) => updateDraftParameter("p", p)}
              onEmpty={() => updateDraftParameter("p", null)}
            />
          </div>

          {finiteParameters !== null && !hasIntegerCoefficients ? (
            <IntegerParameterNotice
              a={finiteParameters.a}
              b={finiteParameters.b}
              onRound={roundDraftCoefficients}
            />
          ) : null}
          {validationError ? <ErrorBanner message={validationError} /> : null}

          <div className="grid gap-3 border-t border-slate-200 pt-4 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-slate-600">Puntos afines</span>
              <span className="font-mono text-slate-900">
                {finiteData.loading ? "..." : points.length}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-600">#E(𝔽ₚ)</span>
              <span className="font-mono text-emerald-700">
                {shouldRenderPlot ? points.length + 1 : "No definido"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-600">{"\u0394 (mod p)"}</span>
              <span className="font-mono text-slate-900">
                {finiteData.loading ? "..." : delta === null ? "No definido" : delta}
              </span>
            </div>
          </div>
        </div>
      </ScientificPanel>

      <ScientificPanel title="Nube de puntos">
        <PlotSurface
          data={data}
          height={560}
          layout={{
            xaxis: {
              range: [-0.8, plotPrime - 0.2],
              dtick: axisStep,
              tick0: 0,
              title: "x",
            },
            yaxis: {
              range: [-0.8, plotPrime - 0.2],
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

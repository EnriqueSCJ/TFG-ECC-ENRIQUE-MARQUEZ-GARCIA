import { useMemo, useState, type ReactNode } from "react";
import { ConceptHint } from "../components/common/ConceptHint";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { IntegerParameterNotice } from "../components/common/IntegerParameterNotice";
import { NumericField } from "../components/common/NumericField";
import { FinitePointSelect } from "../components/common/PointControls";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { SegmentedControl } from "../components/common/SegmentedControl";
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
import type {
  AffinePoint,
  BabyStepGiantStepResponse,
  FactorizationTerm,
  PollardsRhoResponse,
  PollardsRhoStep,
} from "../types/ecc";

type AttackMode = "rho" | "bsgs" | "audit";
type Tone = "slate" | "amber" | "emerald" | "rose";

const CURVE_GROUP_LABEL = "E(𝔽ₚ)";
const GROUP_SIZE_LABEL = "#E(𝔽ₚ)";
const PARTITIONS = [
  { id: 0, label: "S₀", update: "X ← X + G", color: "#4f46e5" },
  { id: 1, label: "S₁", update: "X ← 2X", color: "#0f766e" },
  { id: 2, label: "S₂", update: "X ← X + Q", color: "#b45309" },
] as const;

function finiteOnly<T extends { point: AffinePoint }>(items: T[]): T[] {
  return items.filter((item) => item.point.x !== null && item.point.y !== null);
}

function partitionSteps(steps: PollardsRhoStep[], partition: number): PollardsRhoStep[] {
  return finiteOnly(steps).filter((step) => step.partition === partition);
}

function formatFactorization(factors: FactorizationTerm[]): string {
  if (factors.length === 0) return "1";

  return factors
    .map(({ factor, exponent }) => (exponent === 1 ? factor.toString() : `${factor}${toSuperscript(exponent)}`))
    .join(" · ");
}

function formatNullable(value: number | null | undefined): string {
  return value === null || value === undefined ? "no disponible" : value.toString();
}

function toSuperscript(value: number): string {
  const digits: Record<string, string> = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
  };

  return value.toString().replace(/\d/g, (digit) => digits[digit] ?? digit);
}

function formatPartitionLabel(partition: number): string {
  return PARTITIONS.find((item) => item.id === partition)?.label ?? `S${partition}`;
}

function Hint({
  children,
  title,
  description,
}: {
  children: ReactNode;
  title: string;
  description: string;
}) {
  return (
    <ConceptHint title={title} description={description}>
      {children}
    </ConceptHint>
  );
}

export function AuditAttacksView() {
  const [attackMode, setAttackMode] = useState<AttackMode>("rho");
  const [secretScalar, setSecretScalar] = useState(5);
  const [maxSteps, setMaxSteps] = useState(48);
  const parameters = useCurveStore((state) => state.parameters);
  const setParameters = useCurveStore((state) => state.setParameters);
  const hasIntegerCoefficients = hasIntegerCurveCoefficients(parameters);
  const generator = useMemo(
    () => ({ x: parameters.gx, y: parameters.gy, label: "G" }),
    [parameters.gx, parameters.gy],
  );

  const finiteData = useBackendData(
    () => eccService.getFinitePoints(parameters),
    [hasIntegerCoefficients, parameters],
    hasIntegerCoefficients,
  );
  const points = finiteData.data?.points ?? [];
  const auditData = useBackendData(
    () => eccService.audit(parameters, generator),
    [generator, hasIntegerCoefficients, parameters],
    hasIntegerCoefficients,
  );
  const rhoData = useBackendData(
    () => eccService.pollardsRho(parameters, generator, secretScalar, maxSteps),
    [attackMode, generator, hasIntegerCoefficients, maxSteps, parameters, secretScalar],
    hasIntegerCoefficients && attackMode === "rho",
  );
  const bsgsData = useBackendData(
    () => eccService.babyStepGiantStep(parameters, generator, secretScalar),
    [attackMode, generator, hasIntegerCoefficients, parameters, secretScalar],
    hasIntegerCoefficients && attackMode === "bsgs",
  );

  const audit = auditData.data;
  const rho = rhoData.data;
  const bsgs = bsgsData.data;
  const totalPoints = audit?.totalPoints ?? points.length + 1;
  const axisStep = finiteAxisStep(parameters.p);
  const baseMarkerSize = finiteBackgroundMarkerSize(parameters.p);
  const detailedHover = shouldUseDetailedFiniteHover(parameters.p);

  const plotData = useMemo(() => {
    const traces: Array<Record<string, unknown>> = [
      {
        x: points.map((point) => point.x),
        y: points.map((point) => point.y),
        type: "scatter",
        mode: "markers",
        name: CURVE_GROUP_LABEL,
        text: detailedHover ? points.map((point) => `(${point.x}, ${point.y})`) : undefined,
        hovertemplate: detailedHover
          ? `%{text}<extra>${CURVE_GROUP_LABEL}</extra>`
          : `x=%{x}<br>y=%{y}<extra>${CURVE_GROUP_LABEL}</extra>`,
        marker: {
          color: "rgba(100, 116, 139, 0.28)",
          size: baseMarkerSize,
          line: { color: "#ffffff", width: detailedHover ? 1 : 0 },
        },
      },
      {
        x: [generator.x],
        y: [generator.y],
        type: "scatter",
        mode: "markers+text",
        name: "G",
        text: ["G"],
        textposition: "bottom center",
        hovertemplate: "G = (%{x}, %{y})<extra></extra>",
        marker: { color: "#4f46e5", size: 13, line: { color: "#ffffff", width: 1.5 } },
      },
    ];

    if (attackMode === "rho" && rho) {
      traces.push(
        {
          x: rho.target.x !== null ? [rho.target.x] : [],
          y: rho.target.y !== null ? [rho.target.y] : [],
          type: "scatter",
          mode: "markers+text",
          name: "Q",
          text: ["Q"],
          textposition: "top center",
          hovertemplate: "Q = (%{x}, %{y})<extra>objetivo</extra>",
          marker: { color: "#059669", size: 13, line: { color: "#ffffff", width: 1.5 } },
        },
        {
          x: finiteOnly(rho.steps).map((step) => step.point.x),
          y: finiteOnly(rho.steps).map((step) => step.point.y),
          type: "scatter",
          mode: "lines",
          name: "Trayectoria ρ",
          text: finiteOnly(rho.steps).map((step) => `${step.index}: ${formatPoint(step.point)}`),
          hovertemplate: "%{text}<extra>paso</extra>",
          line: { color: "#92400e", width: 2 },
        },
        ...PARTITIONS.map((partition) => {
          const steps = partitionSteps(rho.steps, partition.id);

          return {
            x: steps.map((step) => step.point.x),
            y: steps.map((step) => step.point.y),
            type: "scatter",
            mode: "markers",
            name: partition.label,
            text: steps.map((step) => `${step.index}: ${formatPoint(step.point)} - ${partition.update}`),
            hovertemplate: "%{text}<extra>particion</extra>",
            marker: {
              color: partition.color,
              size: 8,
              line: { color: "#ffffff", width: 1.2 },
            },
          };
        }),
        {
          x: rho.collision?.point.x !== null && rho.collision?.point.x !== undefined
            ? [rho.collision.point.x]
            : [],
          y: rho.collision?.point.y !== null && rho.collision?.point.y !== undefined
            ? [rho.collision.point.y]
            : [],
          type: "scatter",
          mode: "markers+text",
          name: "Colision",
          text: rho.collision ? ["colisión"] : [],
          textposition: "top center",
          hovertemplate: "%{text}: (%{x}, %{y})<extra></extra>",
          marker: { color: "#be123c", size: 14, symbol: "x" },
        },
      );
    }

    if (attackMode === "bsgs" && bsgs) {
      const babySteps = finiteOnly(bsgs.babySteps);
      const giantSteps = finiteOnly(bsgs.giantSteps);
      const match = bsgs.giantSteps.find((step) => step.matchedBabyIndex !== undefined);

      traces.push(
        {
          x: bsgs.target.x !== null ? [bsgs.target.x] : [],
          y: bsgs.target.y !== null ? [bsgs.target.y] : [],
          type: "scatter",
          mode: "markers+text",
          name: "Q",
          text: ["Q"],
          textposition: "top center",
          hovertemplate: "Q = (%{x}, %{y})<extra>objetivo</extra>",
          marker: { color: "#059669", size: 13, line: { color: "#ffffff", width: 1.5 } },
        },
        {
          x: babySteps.map((step) => step.point.x),
          y: babySteps.map((step) => step.point.y),
          type: "scatter",
          mode: "markers",
          name: "jG",
          text: babySteps.map((step) => `j=${step.index}: ${formatPoint(step.point)}`),
          hovertemplate: "%{text}<extra>baby step</extra>",
          marker: { color: "#4f46e5", size: 8, line: { color: "#ffffff", width: 1 } },
        },
        {
          x: giantSteps.map((step) => step.point.x),
          y: giantSteps.map((step) => step.point.y),
          type: "scatter",
          mode: "lines+markers",
          name: "Q − imG",
          text: giantSteps.map((step) => `i=${step.index}: ${formatPoint(step.point)}`),
          hovertemplate: "%{text}<extra>giant step</extra>",
          line: { color: "#b45309", width: 2 },
          marker: { color: "#b45309", size: 8, line: { color: "#ffffff", width: 1 } },
        },
        {
          x: match?.point.x !== null && match?.point.x !== undefined ? [match.point.x] : [],
          y: match?.point.y !== null && match?.point.y !== undefined ? [match.point.y] : [],
          type: "scatter",
          mode: "markers+text",
          name: "Coincidencia",
          text: match ? ["coincidencia"] : [],
          textposition: "top center",
          hovertemplate: "%{text}: (%{x}, %{y})<extra></extra>",
          marker: { color: "#be123c", size: 14, symbol: "x" },
        },
      );
    }

    return traces;
  }, [attackMode, baseMarkerSize, bsgs, detailedHover, generator, points, rho]);

  const activeTitle: ReactNode =
    attackMode === "rho"
      ? (
          <Hint
            title="Pollard ρ"
            description="Ataque probabilístico al logaritmo discreto: camina por el grupo hasta encontrar una colisión que permite recuperar k."
          >
            Pollard ρ
          </Hint>
        )
      : attackMode === "bsgs"
        ? (
            <Hint
              title="Baby-step/Giant-step"
              description="Método de búsqueda que guarda pasos pequeños jG y los compara con pasos grandes Q − imG para despejar k."
            >
              Baby-step/Giant-step
            </Hint>
          )
        : (
            <Hint
              title="Auditoría de parámetros"
              description="Resume propiedades básicas del dominio: tamaño del grupo, orden del punto base, cofactor y señales de riesgo conocidas."
            >
              Checklist de parámetros
            </Hint>
          );

  return (
    <div className="grid gap-5 xl:grid-cols-[23rem_1fr]">
      <ScientificPanel
        title="Auditoría y ataques"
        description="Análisis didáctico del ECDLP en grupos pequeños."
        action={
          <SegmentedControl
            value={attackMode}
            onChange={setAttackMode}
            options={[
              { value: "rho", label: "ρ" },
              { value: "bsgs", label: "BSGS" },
              { value: "audit", label: "Auditoría" },
            ]}
          />
        }
      >
        <div className="grid gap-4">
          <FormulaBlock
            compact
            math={
              attackMode === "rho"
                ? "X_i=\\alpha_iG+\\beta_iQ"
                : attackMode === "bsgs"
                  ? "Q-imG=jG"
                  : "\\#E(\\mathbb{F}_p),\\ n=\\operatorname{ord}(G),\\ h=\\#E(\\mathbb{F}_p)/n"
            }
          />

          {attackMode !== "audit" ? (
            <div className={attackMode === "rho" ? "grid grid-cols-2 gap-3" : "grid gap-3"}>
              <NumericField
                label="Secreto k"
                min={1}
                value={secretScalar}
                onChange={setSecretScalar}
              />
              {attackMode === "rho" ? (
                <NumericField
                  label="Pasos"
                  min={8}
                  max={160}
                  value={maxSteps}
                  onChange={setMaxSteps}
                />
              ) : null}
            </div>
          ) : null}

          <FinitePointSelect
            label="Punto base G"
            value={generator}
            points={points}
            onChange={(point) => setParameters({ gx: point.x ?? 0, gy: point.y ?? 0 })}
          />

          {!hasIntegerCoefficients ? (
            <IntegerParameterNotice
              a={parameters.a}
              b={parameters.b}
              onRound={() => setParameters(roundCurveCoefficients(parameters))}
            />
          ) : null}
          {finiteData.error ? <ErrorBanner message={finiteData.error} /> : null}
          {auditData.error ? <ErrorBanner message={auditData.error} /> : null}
          {rhoData.error ? <ErrorBanner message={rhoData.error} /> : null}
          {bsgsData.error ? <ErrorBanner message={bsgsData.error} /> : null}

          <MetricPanel>
            <MetricRow
              label={
                <Hint
                  title="Tamaño del grupo"
                  description="#E(𝔽ₚ) cuenta todos los puntos de la curva sobre el cuerpo finito, incluyendo el punto del infinito."
                >
                  {GROUP_SIZE_LABEL}
                </Hint>
              }
              value={auditData.loading ? "..." : totalPoints.toString()}
            />
            <MetricRow
              label={
                <Hint
                  title="Orden de G"
                  description="ord(G) es el menor n positivo tal que nG = 𝒪. Es el tamaño del subgrupo generado por G."
                >
                  ord(G)
                </Hint>
              }
              value={formatNullable(audit?.order)}
            />
            <MetricRow label="Factores" value={formatFactorization(audit?.factors ?? [])} />
            <MetricRow
              label={
                <Hint
                  title="Cofactor"
                  description="h = #E(𝔽ₚ) / ord(G). Si h > 1, hay subgrupos adicionales que conviene controlar."
                >
                  Cofactor h
                </Hint>
              }
              value={formatNullable(audit?.cofactor)}
            />
          </MetricPanel>
        </div>
      </ScientificPanel>

      {attackMode === "audit" ? (
        <ScientificPanel title={activeTitle}>
          <AuditDashboard audit={audit} p={parameters.p} />
        </ScientificPanel>
      ) : (
        <ScientificPanel title={activeTitle}>
          <div className="grid gap-4">
            <AttackFlow mode={attackMode} rho={rho} bsgs={bsgs} />
            <PlotSurface
              data={plotData}
              height={520}
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
            {attackMode === "rho" && rho ? <PollardRhoDetails result={rho} /> : null}
            {attackMode === "bsgs" && bsgs ? <BsgsDetails result={bsgs} /> : null}
          </div>
        </ScientificPanel>
      )}
    </div>
  );
}

function AttackFlow({
  mode,
  rho,
  bsgs,
}: {
  mode: AttackMode;
  rho: PollardsRhoResponse | null;
  bsgs: BabyStepGiantStepResponse | null;
}) {
  const rhoCollision = rho?.collision;
  const bsgsMatch = bsgs?.giantSteps.find((step) => step.matchedBabyIndex !== undefined);
  const steps =
    mode === "rho"
      ? [
          {
            label: (
              <Hint
                title="Objetivo Q"
                description="Q es el punto público: Q = kG. El ataque intenta recuperar el escalar secreto k."
              >
                Objetivo
              </Hint>
            ),
            value: rho ? `Q = ${formatPoint(rho.target)}` : "Q = kG",
          },
          {
            label: (
              <Hint
                title="Caminata rho"
                description="Cada punto se escribe como Xᵢ = αᵢG + βᵢQ. Al chocar dos Xᵢ se obtiene una ecuación sobre k."
              >
                Caminata
              </Hint>
            ),
            value: "Xᵢ = αᵢG + βᵢQ",
          },
          {
            label: (
              <Hint
                title="Colisión"
                description="Dos pasos llegan al mismo punto X. Esa igualdad permite plantear una congruencia para recuperar k."
              >
                Colisión
              </Hint>
            ),
            value: rhoCollision ? `${rhoCollision.firstIndex} = ${rhoCollision.secondIndex}` : "pendiente",
          },
          { label: "Salida", value: formatNullable(rhoCollision?.recoveredSecret) },
        ]
      : [
          {
            label: (
              <Hint
                title="Tamaño m"
                description="Se toma m = ⌈√n⌉ para dividir la búsqueda en dos tablas de tamaño aproximado raíz de n."
              >
                Tamaño
              </Hint>
            ),
            value: bsgs ? `m = ${bsgs.m}` : "m = ⌈√n⌉",
          },
          {
            label: (
              <Hint
                title="Baby steps"
                description="Tabla de puntos jG para valores pequeños de j. Sirve como lista de posibles coincidencias."
              >
                Baby
              </Hint>
            ),
            value: "jG",
          },
          {
            label: (
              <Hint
                title="Giant steps"
                description="Se calculan puntos Q − imG. Cuando uno coincide con jG, se obtiene k = im + j."
              >
                Giant
              </Hint>
            ),
            value: "Q − imG",
          },
          { label: "k", value: bsgsMatch ? formatNullable(bsgs?.result) : "pendiente" },
        ];

  return (
    <div className="grid gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-3 sm:grid-cols-4">
      {steps.map((step, index) => (
        <div key={index} className="relative rounded-md border border-slate-200 bg-white px-3 py-2">
          {index < steps.length - 1 ? (
            <div className="absolute -right-2 top-1/2 hidden h-px w-4 bg-slate-300 sm:block" />
          ) : null}
          <div className="text-xs font-medium uppercase text-slate-500">{step.label}</div>
          <div className="mt-1 break-words font-mono text-sm text-slate-950">{step.value}</div>
        </div>
      ))}
    </div>
  );
}

function PollardRhoDetails({ result }: { result: PollardsRhoResponse }) {
  const recentSteps = result.steps.slice(-6);
  const collision = result.collision;

  return (
    <div className="grid gap-4 lg:grid-cols-[0.85fr_1fr]">
      <ResultCard tone={collision ? (collision.recoveredSecret !== null ? "emerald" : "amber") : "slate"}>
        <MetricRow
          label={
            <Hint
              title="Punto objetivo"
              description="Q es el punto que oculta el secreto k en la relación Q = kG."
            >
              Q
            </Hint>
          }
          value={formatPoint(result.target)}
        />
        <MetricRow
          label="Colision"
          value={collision ? `${collision.firstIndex} = ${collision.secondIndex}` : "no detectada"}
        />
        <MetricRow
          label={
            <Hint
              title="Diferencia Δα"
              description="Diferencia entre los coeficientes α de los dos pasos que han colisionado."
            >
              Δα
            </Hint>
          }
          value={formatNullable(collision?.alphaDelta)}
        />
        <MetricRow
          label={
            <Hint
              title="Diferencia Δβ"
              description="Diferencia entre los coeficientes β de los dos pasos que han colisionado."
            >
              Δβ
            </Hint>
          }
          value={formatNullable(collision?.betaDelta)}
        />
        <MetricRow label="k" value={formatNullable(collision?.recoveredSecret)} />
        <MetricRow label="n" value={result.order.toString()} />
      </ResultCard>

      <StepTable
        title="Ultimos pasos"
        columns={[
          "i",
          "S",
          <Hint
            key="alpha"
            title="Coeficiente α"
            description="α indica cuántas copias de G forman el punto actual X = αG + βQ."
          >
            α
          </Hint>,
          <Hint
            key="beta"
            title="Coeficiente β"
            description="β indica cuántas copias de Q forman el punto actual X = αG + βQ."
          >
            β
          </Hint>,
          "X",
        ]}
        rows={recentSteps.map((step) => [
          step.index.toString(),
          formatPartitionLabel(step.partition),
          step.alpha.toString(),
          step.beta.toString(),
          formatPoint(step.point),
        ])}
      />
    </div>
  );
}

function BsgsDetails({ result }: { result: BabyStepGiantStepResponse }) {
  const match = result.giantSteps.find((step) => step.matchedBabyIndex !== undefined);

  return (
    <div className="grid gap-4 lg:grid-cols-[0.85fr_1.15fr]">
      <ResultCard tone={result.found ? "emerald" : "amber"}>
        <MetricRow label="Q" value={formatPoint(result.target)} />
        <MetricRow
          label={
            <Hint
              title="Orden de G"
              description="El ataque busca k dentro del subgrupo generado por G, cuyo tamaño es ord(G)."
            >
              ord(G)
            </Hint>
          }
          value={result.order.toString()}
        />
        <MetricRow
          label={
            <Hint
              title="Parámetro m"
              description="m = ⌈√ord(G)⌉. Equilibra el número de baby steps y giant steps."
            >
              m
            </Hint>
          }
          value={result.m.toString()}
        />
        <MetricRow
          label={
            <Hint
              title="Índice i"
              description="Número de giant steps usados en la coincidencia Q − imG = jG."
            >
              i
            </Hint>
          }
          value={formatNullable(match?.index)}
        />
        <MetricRow
          label={
            <Hint
              title="Índice j"
              description="Baby step que coincide con un giant step. Con la coincidencia se reconstruye k = im + j."
            >
              j
            </Hint>
          }
          value={formatNullable(match?.matchedBabyIndex)}
        />
        <MetricRow label="k" value={formatNullable(result.result)} />
      </ResultCard>
      <BsgsTableVisual result={result} />
    </div>
  );
}

function BsgsTableVisual({ result }: { result: BabyStepGiantStepResponse }) {
  const match = result.giantSteps.find((step) => step.matchedBabyIndex !== undefined);
  const babyPreview = result.babySteps.slice(0, 6);
  const giantPreview = result.giantSteps.slice(0, 6);

  if (
    match?.matchedBabyIndex !== undefined &&
    !babyPreview.some((step) => step.index === match.matchedBabyIndex)
  ) {
    const matchedBaby = result.babySteps.find((step) => step.index === match.matchedBabyIndex);
    if (matchedBaby) babyPreview.push(matchedBaby);
  }

  if (match && !giantPreview.some((step) => step.index === match.index)) {
    giantPreview.push(match);
  }

  babyPreview.sort((left, right) => left.index - right.index);
  giantPreview.sort((left, right) => left.index - right.index);

  return (
    <div className="grid gap-3 rounded-md border border-slate-200 bg-white px-3 py-3">
      <FormulaBlock compact math="m=\lceil\sqrt{n}\rceil,\quad Q-imG=jG" />
      <div className="grid gap-3 xl:grid-cols-2">
        <PointStepTable
          title={
            <Hint
              title="Tabla baby"
              description="Lista puntos jG para compararlos después con los giant steps."
            >
              Baby
            </Hint>
          }
          indexLabel="j"
          formulaLabel="jG"
          rows={babyPreview}
          highlightedIndex={match?.matchedBabyIndex}
        />
        <PointStepTable
          title={
            <Hint
              title="Tabla giant"
              description="Lista puntos Q − imG. Una coincidencia con jG revela el valor de k."
            >
              Giant
            </Hint>
          }
          indexLabel="i"
          formulaLabel="Q − imG"
          rows={giantPreview}
          highlightedIndex={match?.index}
        />
      </div>
    </div>
  );
}

function PointStepTable({
  title,
  indexLabel,
  formulaLabel,
  rows,
  highlightedIndex,
}: {
  title: ReactNode;
  indexLabel: string;
  formulaLabel: string;
  rows: Array<{ index: number; point: AffinePoint }>;
  highlightedIndex?: number;
}) {
  return (
    <StepTable
      title={title}
      columns={[indexLabel, formulaLabel, "Punto"]}
      rows={rows.map((row) => [
        row.index.toString(),
        indexLabel === "j" ? `${row.index}G` : `Q − ${row.index}mG`,
        formatPoint(row.point),
      ])}
      highlightedRowIndex={
        highlightedIndex === undefined
          ? undefined
          : rows.findIndex((row) => row.index === highlightedIndex)
      }
    />
  );
}

function AuditDashboard({
  audit,
  p,
}: {
  audit: {
    totalPoints: number;
    order: number;
    factors: FactorizationTerm[];
    cofactor: number | null;
    largestPrimeFactor: number | null;
    isAnomalous: boolean;
  } | null;
  p: number;
}) {
  if (!audit) {
    return (
      <div className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
        Esperando respuesta del backend.
      </div>
    );
  }

  const isSmooth = audit.factors.length > 1 || audit.factors.some((factor) => factor.exponent > 1);
  const cofactorRisk = audit.cofactor !== null && audit.cofactor > 1;
  const overallTone: Tone = audit.isAnomalous ? "rose" : isSmooth || cofactorRisk ? "amber" : "emerald";
  const overallStatus = audit.isAnomalous ? "Riesgo" : isSmooth || cofactorRisk ? "Revisar" : "OK";

  return (
    <div className="grid gap-4">
      <div className={toneClass(overallTone, "rounded-md border px-4 py-4")}>
        <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-semibold text-slate-950">Diagnostico</h3>
              <StatusPill tone={overallTone}>{overallStatus}</StatusPill>
            </div>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-700">
              {audit.isAnomalous
                ? "La curva cumple la condición anómala."
                : isSmooth
                  ? "El punto base tiene orden compuesto; Pohlig-Hellman merece atencion."
                  : cofactorRisk
                    ? "El cofactor exige validacion cuidadosa de puntos."
                    : "Los checks basicos no muestran alertas para este G."}
            </p>
          </div>
          <div className="grid min-w-0 gap-2 sm:grid-cols-4 xl:min-w-[28rem]">
            <StatTile label={GROUP_SIZE_LABEL} value={audit.totalPoints.toString()} />
            <StatTile label="p" value={p.toString()} />
            <StatTile label="ord(G)" value={audit.order.toString()} />
            <StatTile label="h" value={formatNullable(audit.cofactor)} />
          </div>
        </div>
      </div>

      <div className="grid gap-3">
        <AuditCheckRow
          title={
            <Hint
              title="Ataque de Smart"
              description="Afecta a curvas anómalas, donde #E(𝔽ₚ) = p. Es una señal crítica en ECC clásica."
            >
              Smart
            </Hint>
          }
          description="Curva anómala"
          expression={`${GROUP_SIZE_LABEL} = p`}
          detail={audit.isAnomalous ? `${audit.totalPoints} = ${p}` : `${audit.totalPoints} ≠ ${p}`}
          tone={audit.isAnomalous ? "rose" : "emerald"}
          status={audit.isAnomalous ? "Riesgo" : "OK"}
        />
        <AuditCheckRow
          title={
            <Hint
              title="Pohlig-Hellman"
              description="Si ord(G) factoriza en primos pequeños, el ECDLP puede resolverse por partes más fácilmente."
            >
              Pohlig-Hellman
            </Hint>
          }
          description="Orden factorizable"
          expression={`ord(G) = ${formatFactorization(audit.factors)}`}
          detail={`mayor factor ${formatNullable(audit.largestPrimeFactor)}`}
          tone={isSmooth ? "amber" : "emerald"}
          status={isSmooth ? "Revisar" : "OK"}
        />
        <AuditCheckRow
          title={
            <Hint
              title="Riesgo de subgrupos"
              description="Si h > 1, existen puntos fuera del subgrupo principal. En protocolos reales se validan para evitar ataques."
            >
              Subgrupos
            </Hint>
          }
          description="Cofactor"
          expression={`h = ${formatNullable(audit.cofactor)}`}
          detail={cofactorRisk ? "validar puntos" : "sin alerta"}
          tone={cofactorRisk ? "amber" : "emerald"}
          status={cofactorRisk ? "Revisar" : "OK"}
        />
      </div>
    </div>
  );
}

function StatTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-white/80 bg-white/80 px-3 py-2">
      <div className="text-xs font-medium text-slate-500">{label}</div>
      <div className="mt-1 whitespace-nowrap text-right font-mono text-sm text-slate-950">{value}</div>
    </div>
  );
}

function AuditCheckRow({
  title,
  description,
  expression,
  detail,
  tone,
  status,
}: {
  title: ReactNode;
  description: string;
  expression: string;
  detail: string;
  tone: Tone;
  status: string;
}) {
  return (
    <div className={toneClass(tone, "grid gap-3 rounded-md border px-4 py-3 md:grid-cols-[1fr_auto_auto] md:items-center")}>
      <div className="min-w-0">
        <h3 className="text-sm font-semibold text-slate-950">{title}</h3>
        <p className="mt-1 text-xs text-slate-600">{description}</p>
      </div>
      <div className="grid gap-1 text-left md:text-right">
        <span className="whitespace-nowrap font-mono text-sm text-slate-950">{expression}</span>
        <span className="whitespace-nowrap text-xs text-slate-600">{detail}</span>
      </div>
      <div className="justify-self-start md:justify-self-end">
        <StatusPill tone={tone}>{status}</StatusPill>
      </div>
    </div>
  );
}

function ResultCard({ tone, children }: { tone: Tone; children: ReactNode }) {
  return <div className={toneClass(tone, "grid gap-2 rounded-md border px-4 py-3 text-sm")}>{children}</div>;
}

function MetricPanel({ children }: { children: ReactNode }) {
  return (
    <div className="grid gap-2 border-t border-slate-200 pt-4 text-sm">
      {children}
    </div>
  );
}

function MetricRow({ label, value }: { label: ReactNode; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 border-t border-white/70 pt-2 first:border-t-0 first:pt-0">
      <span className="min-w-0 text-slate-600">{label}</span>
      <span className="shrink-0 whitespace-nowrap text-right font-mono text-slate-950">{value}</span>
    </div>
  );
}

function StepTable({
  title,
  columns,
  rows,
  highlightedRowIndex,
}: {
  title: ReactNode;
  columns: ReactNode[];
  rows: string[][];
  highlightedRowIndex?: number;
}) {
  return (
    <div className="rounded-md border border-slate-200">
      <div className="border-b border-slate-200 bg-slate-50 px-3 py-2 text-xs font-medium uppercase text-slate-500">
        {title}
      </div>
      <table className="w-full text-left text-sm">
        <thead className="bg-white text-xs uppercase text-slate-500">
          <tr>
            {columns.map((column, columnIndex) => (
              <th key={columnIndex} className="px-3 py-2">{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr
              key={`${title}-${rowIndex}`}
              className={
                highlightedRowIndex === rowIndex
                  ? "border-t border-emerald-200 bg-emerald-50"
                  : "border-t border-slate-100"
              }
            >
              {row.map((cell, cellIndex) => (
                <td key={`${title}-${rowIndex}-${cellIndex}`} className="px-3 py-2 font-mono text-slate-900">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function StatusPill({ tone, children }: { tone: Tone; children: ReactNode }) {
  const className =
    tone === "rose"
      ? "bg-rose-100 text-rose-800"
      : tone === "amber"
        ? "bg-amber-100 text-amber-800"
        : tone === "emerald"
          ? "bg-emerald-100 text-emerald-800"
          : "bg-slate-100 text-slate-700";

  return <span className={`rounded-full px-2 py-1 text-xs font-medium ${className}`}>{children}</span>;
}

function toneClass(tone: Tone, base: string): string {
  const tones: Record<Tone, string> = {
    slate: "border-slate-200 bg-white",
    amber: "border-amber-200 bg-amber-50/45",
    emerald: "border-emerald-200 bg-emerald-50/45",
    rose: "border-rose-200 bg-rose-50/45",
  };

  return `${base} ${tones[tone]}`;
}

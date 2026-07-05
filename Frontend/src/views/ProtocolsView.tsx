import {
  ArrowRightLeft,
  CheckCircle2,
  Eye,
  KeyRound,
  Lock,
  RefreshCw,
  Send,
  ShieldCheck,
  Unlock,
  UserRound,
} from "lucide-react";
import { useEffect, useMemo, useState, type ReactNode } from "react";
import { InlineMath } from "react-katex";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { FormulaBlock } from "../components/common/FormulaBlock";
import { IntegerParameterNotice } from "../components/common/IntegerParameterNotice";
import { NumericField } from "../components/common/NumericField";
import { FinitePointSelect } from "../components/common/PointControls";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { SegmentedControl } from "../components/common/SegmentedControl";
import { useBackendData } from "../hooks/useBackendData";
import { formatPoint } from "../lib/eccMath";
import { hasIntegerCurveCoefficients, roundCurveCoefficients } from "../lib/finiteParameters";
import { eccService } from "../services/eccService";
import { useCurveStore } from "../store/curveStore";
import { AffinePoint } from "../types/ecc";

type ProtocolTab = "ecdh" | "ecdsa";
type EcdhStage = "setup" | "public" | "exchanged" | "shared";
type EcdsaStage = "draft" | "signed" | "published" | "verified";

const stageRank: Record<EcdhStage, number> = {
  setup: 0,
  public: 1,
  exchanged: 2,
  shared: 3,
};

function hasReached(current: EcdhStage, target: EcdhStage): boolean {
  return stageRank[current] >= stageRank[target];
}

const ecdsaStageRank: Record<EcdsaStage, number> = {
  draft: 0,
  signed: 1,
  published: 2,
  verified: 3,
};

function hasReachedEcdsa(current: EcdsaStage, target: EcdsaStage): boolean {
  return ecdsaStageRank[current] >= ecdsaStageRank[target];
}

function formatSignature(signature: { r: number; s: number }): string {
  return `(${signature.r}, ${signature.s})`;
}

function MathTerm({ math }: { math: string }) {
  return <InlineMath math={math} />;
}

export function ProtocolsView() {
  const [tab, setTab] = useState<ProtocolTab>("ecdh");
  const [ecdhStage, setEcdhStage] = useState<EcdhStage>("setup");
  const [ecdsaStage, setEcdsaStage] = useState<EcdsaStage>("draft");
  const [aliceSecret, setAliceSecret] = useState(5);
  const [bobSecret, setBobSecret] = useState(8);
  const [privateSecret, setPrivateSecret] = useState(2);
  const [nonce, setNonce] = useState(1);
  const [message, setMessage] = useState("ECC didáctico");
  const parameters = useCurveStore((state) => state.parameters);
  const setParameters = useCurveStore((state) => state.setParameters);
  const hasIntegerCoefficients = hasIntegerCurveCoefficients(parameters);
  const finiteData = useBackendData(
    () => eccService.getFinitePoints(parameters),
    [hasIntegerCoefficients, parameters],
    hasIntegerCoefficients,
  );
  const points = finiteData.data?.points ?? [];
  const generator = useMemo(
    () => ({ x: parameters.gx, y: parameters.gy, label: "G" }),
    [parameters.gx, parameters.gy],
  );

  const ecdhData = useBackendData(
    () => eccService.simulateEcdh(parameters, generator, aliceSecret, bobSecret),
    [aliceSecret, bobSecret, generator, hasIntegerCoefficients, parameters],
    hasIntegerCoefficients,
  );
  const ecdh = { value: ecdhData.data, error: ecdhData.error };

  useEffect(() => {
    setEcdhStage("setup");
  }, [
    aliceSecret,
    bobSecret,
    parameters.a,
    parameters.b,
    parameters.gx,
    parameters.gy,
    parameters.p,
  ]);

  const ecdsaData = useBackendData(
    () => eccService.simulateEcdsa(parameters, generator, privateSecret, nonce, message),
    [generator, hasIntegerCoefficients, message, nonce, parameters, privateSecret],
    hasIntegerCoefficients,
  );
  const ecdsa = { value: ecdsaData.data, error: ecdsaData.error };

  useEffect(() => {
    setEcdsaStage("draft");
  }, [
    message,
    nonce,
    parameters.a,
    parameters.b,
    parameters.gx,
    parameters.gy,
    parameters.p,
    privateSecret,
  ]);

  return (
    <div className="grid gap-5">
      <ScientificPanel
        title="Protocolos"
        description="Simulaciones de dominio pequeño para visualizar el flujo criptográfico."
        action={
          <SegmentedControl
            value={tab}
            onChange={setTab}
            options={[
              { value: "ecdh", label: "ECDH" },
              { value: "ecdsa", label: "ECDSA" },
            ]}
          />
        }
      >
        {tab === "ecdh" ? (
          <div className="grid gap-5 xl:grid-cols-[22rem_minmax(0,1fr)]">
            <div className="grid min-w-0 gap-4">
              <FormulaBlock math="\begin{aligned}S_A&=d_A Q_B\\S_B&=d_B Q_A\\S_A&=S_B=d_A d_B G\end{aligned}" />
              <div className="grid grid-cols-2 gap-3">
                <NumericField label={<MathTerm math="d_A" />} value={aliceSecret} onChange={setAliceSecret} />
                <NumericField label={<MathTerm math="d_B" />} value={bobSecret} onChange={setBobSecret} />
              </div>
              <FinitePointSelect
                label="G base"
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
              {ecdh.error ? <ErrorBanner message={ecdh.error} /> : null}

              <div className="grid gap-2 border-t border-slate-200 pt-4">
                <button
                  type="button"
                  onClick={() => setEcdhStage("public")}
                  disabled={!ecdh.value}
                  className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-indigo-700 px-3 text-sm font-medium text-white transition hover:bg-indigo-600 disabled:cursor-not-allowed disabled:bg-slate-300"
                >
                  <KeyRound className="h-4 w-4" aria-hidden="true" />
                  Generar claves
                </button>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setEcdhStage("exchanged")}
                    disabled={!ecdh.value || !hasReached(ecdhStage, "public")}
                    className="inline-flex h-10 items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-45"
                  >
                    <Send className="h-4 w-4" aria-hidden="true" />
                    Intercambiar
                  </button>
                  <button
                    type="button"
                    onClick={() => setEcdhStage("shared")}
                    disabled={!ecdh.value || !hasReached(ecdhStage, "exchanged")}
                    className="inline-flex h-10 items-center justify-center gap-2 rounded-md border border-emerald-300 bg-emerald-50 px-3 text-sm font-medium text-emerald-800 transition hover:bg-emerald-100 disabled:cursor-not-allowed disabled:opacity-45"
                  >
                    <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                    Derivar
                  </button>
                </div>
                <button
                  type="button"
                  onClick={() => setEcdhStage("setup")}
                  className="inline-flex h-9 items-center justify-center gap-2 rounded-md px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
                >
                  <RefreshCw className="h-4 w-4" aria-hidden="true" />
                  Reiniciar flujo
                </button>
              </div>
            </div>

              {ecdh.value ? (
                <div className="grid min-w-0 gap-4">
                  <EcdhTimeline stage={ecdhStage} />
                  <div className="grid min-w-0 gap-4 2xl:grid-cols-[minmax(0,1fr)_14rem_minmax(0,1fr)]">
                    <EcdhPartyCard
                      name="Alice"
                      tone="alice"
                      privateLabel={<>Clave privada <MathTerm math="d_A" /></>}
                      privateValue={ecdh.value.alicePrivate.toString()}
                      publicLabel={<>Clave pública <MathTerm math="Q_A" /></>}
                      publicValue={
                        hasReached(ecdhStage, "public")
                          ? formatPoint(ecdh.value.alicePublic)
                          : "pendiente"
                      }
                      formula={
                        hasReached(ecdhStage, "public")
                          ? <><MathTerm math="Q_A" /> = {ecdh.value.alicePrivate} · G = {formatPoint(ecdh.value.alicePublic)}</>
                        : <><MathTerm math="Q_A" /> = <MathTerm math="d_A" /> · G</>
                      }
                    />
                    <EcdhChannel
                      stage={ecdhStage}
                      alicePublic={ecdh.value.alicePublic}
                      bobPublic={ecdh.value.bobPublic}
                    />
                    <EcdhPartyCard
                      name="Bob"
                      tone="bob"
                      privateLabel={<>Clave privada <MathTerm math="d_B" /></>}
                      privateValue={ecdh.value.bobPrivate.toString()}
                      publicLabel={<>Clave pública <MathTerm math="Q_B" /></>}
                      publicValue={
                        hasReached(ecdhStage, "public")
                          ? formatPoint(ecdh.value.bobPublic)
                          : "pendiente"
                      }
                      formula={
                        hasReached(ecdhStage, "public")
                          ? <><MathTerm math="Q_B" /> = {ecdh.value.bobPrivate} · G = {formatPoint(ecdh.value.bobPublic)}</>
                        : <><MathTerm math="Q_B" /> = <MathTerm math="d_B" /> · G</>
                      }
                    />
                  </div>
                  <EcdhSharedSecretPanel
                    stage={ecdhStage}
                    aliceFormula={<><MathTerm math="S_A" /> = {ecdh.value.alicePrivate} · {formatPoint(ecdh.value.bobPublic)}</>}
                    aliceSecret={formatPoint(ecdh.value.sharedByAlice)}
                    bobFormula={<><MathTerm math="S_B" /> = {ecdh.value.bobPrivate} · {formatPoint(ecdh.value.alicePublic)}</>}
                    bobSecret={formatPoint(ecdh.value.sharedByBob)}
                    matches={ecdh.value.matches}
                    order={ecdh.value.order}
                  />
                </div>
              ) : null}
          </div>
        ) : (
          <div className="grid gap-5 xl:grid-cols-[22rem_minmax(0,1fr)]">
            <div className="grid min-w-0 gap-4">
              <FormulaBlock math="\operatorname{sig}=(r,s),\quad s\equiv k^{-1}(H(m)+rd)\pmod{n}" />
              <div className="grid grid-cols-2 gap-3">
                <NumericField label="d" value={privateSecret} onChange={setPrivateSecret} />
                <NumericField label="Nonce k" value={nonce} onChange={setNonce} />
              </div>
              <FinitePointSelect
                label="G base"
                value={generator}
                points={points}
                onChange={(point) => setParameters({ gx: point.x ?? 0, gy: point.y ?? 0 })}
              />
              <label className="grid gap-1.5 text-sm text-slate-700">
                <span className="font-medium text-slate-800">Mensaje</span>
                <textarea
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  className="min-h-24 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-indigo-700 focus:ring-2 focus:ring-indigo-100"
                />
              </label>
              {!hasIntegerCoefficients ? (
                <IntegerParameterNotice
                  a={parameters.a}
                  b={parameters.b}
                  onRound={() => setParameters(roundCurveCoefficients(parameters))}
                />
              ) : null}
              {finiteData.error ? <ErrorBanner message={finiteData.error} /> : null}
              {ecdsa.error ? <ErrorBanner message={ecdsa.error} /> : null}

              <div className="grid gap-2 border-t border-slate-200 pt-4">
                <button
                  type="button"
                  onClick={() => setEcdsaStage("signed")}
                  disabled={!ecdsa.value}
                  className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-indigo-700 px-3 text-sm font-medium text-white transition hover:bg-indigo-600 disabled:cursor-not-allowed disabled:bg-slate-300"
                >
                  <KeyRound className="h-4 w-4" aria-hidden="true" />
                  Firmar mensaje
                </button>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setEcdsaStage("published")}
                    disabled={!ecdsa.value || !hasReachedEcdsa(ecdsaStage, "signed")}
                    className="inline-flex h-10 items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-45"
                  >
                    <Send className="h-4 w-4" aria-hidden="true" />
                    Publicar
                  </button>
                  <button
                    type="button"
                    onClick={() => setEcdsaStage("verified")}
                    disabled={!ecdsa.value || !hasReachedEcdsa(ecdsaStage, "published")}
                    className="inline-flex h-10 items-center justify-center gap-2 rounded-md border border-emerald-300 bg-emerald-50 px-3 text-sm font-medium text-emerald-800 transition hover:bg-emerald-100 disabled:cursor-not-allowed disabled:opacity-45"
                  >
                    <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                    Verificar
                  </button>
                </div>
                <button
                  type="button"
                  onClick={() => setEcdsaStage("draft")}
                  className="inline-flex h-9 items-center justify-center gap-2 rounded-md px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
                >
                  <RefreshCw className="h-4 w-4" aria-hidden="true" />
                  Reiniciar flujo
                </button>
              </div>
            </div>

              {ecdsa.value ? (
                <div className="grid min-w-0 gap-4">
                  <EcdsaTimeline stage={ecdsaStage} />
                  <div className="grid min-w-0 gap-4 2xl:grid-cols-[minmax(0,1fr)_16rem_minmax(0,1fr)]">
                    <EcdsaSignerCard
                      stage={ecdsaStage}
                      privateKey={ecdsa.value.privateKey}
                      nonce={ecdsa.value.nonce}
                      publicKey={ecdsa.value.publicKey}
                      hash={ecdsa.value.hash}
                      signature={ecdsa.value.signature}
                    />
                    <EcdsaPackageCard
                      stage={ecdsaStage}
                      message={message}
                      publicKey={ecdsa.value.publicKey}
                      signature={ecdsa.value.signature}
                    />
                    <EcdsaVerifierCard
                      stage={ecdsaStage}
                      order={ecdsa.value.order}
                      hash={ecdsa.value.hash}
                      signature={ecdsa.value.signature}
                      verification={ecdsa.value.verification}
                    />
                  </div>
                  <EcdsaVerificationPanel
                    stage={ecdsaStage}
                    order={ecdsa.value.order}
                    signature={ecdsa.value.signature}
                    verification={ecdsa.value.verification}
                  />
                </div>
              ) : null}
          </div>
        )}
      </ScientificPanel>
    </div>
  );
}

function EcdhTimeline({ stage }: { stage: EcdhStage }) {
  const steps: Array<{ label: ReactNode; target: EcdhStage }> = [
    { label: <>Generar <MathTerm math="Q_A" /> y <MathTerm math="Q_B" /></>, target: "public" },
    { label: "Intercambiar públicas", target: "exchanged" },
    { label: "Derivar secreto", target: "shared" },
  ];

  return (
    <div className="grid gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-3 sm:grid-cols-3">
      {steps.map((step) => {
        const done = hasReached(stage, step.target);
        const current = stageRank[stage] + 1 === stageRank[step.target];

        return (
          <div
            key={step.target}
            className={
              done
                ? "flex items-center gap-2 text-sm font-medium text-emerald-700"
                : current
                  ? "flex items-center gap-2 text-sm font-medium text-indigo-800"
                  : "flex items-center gap-2 text-sm font-medium text-slate-500"
            }
          >
            <span
              className={
                done
                  ? "flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100"
                  : current
                    ? "flex h-6 w-6 items-center justify-center rounded-full bg-indigo-100"
                    : "flex h-6 w-6 items-center justify-center rounded-full bg-white"
              }
            >
              {done ? <CheckCircle2 className="h-4 w-4" /> : stageRank[step.target]}
            </span>
            {step.label}
          </div>
        );
      })}
    </div>
  );
}

function EcdhPartyCard({
  name,
  tone,
  privateLabel,
  privateValue,
  publicLabel,
  publicValue,
  formula,
}: {
  name: string;
  tone: "alice" | "bob";
  privateLabel: ReactNode;
  privateValue: string;
  publicLabel: ReactNode;
  publicValue: string;
  formula: ReactNode;
}) {
  const isAlice = tone === "alice";
  const shellClass = isAlice
    ? "border-indigo-200 bg-indigo-50/60"
    : "border-amber-200 bg-amber-50/60";
  const avatarClass = isAlice ? "bg-indigo-700 text-white" : "bg-amber-700 text-white";

  return (
    <div className={`grid min-w-0 gap-3 rounded-md border p-4 ${shellClass}`}>
      <div className="flex items-start gap-3">
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-md ${avatarClass}`}>
          <UserRound className="h-5 w-5" aria-hidden="true" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-950">{name}</h3>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            Calcula localmente y solo expone su clave pública.
          </p>
        </div>
      </div>

      <ProtocolValueBox
        icon={<Lock className="h-4 w-4" aria-hidden="true" />}
        label={privateLabel}
        value={privateValue}
      />
      <ProtocolValueBox
        icon={<Unlock className="h-4 w-4" aria-hidden="true" />}
        label={publicLabel}
        value={publicValue}
        muted={publicValue === "pendiente"}
      />

      <div className="rounded-md border border-white/80 bg-white/75 px-3 py-2">
        <p className="font-mono text-xs text-slate-700">{formula}</p>
      </div>
    </div>
  );
}

function ProtocolValueBox({
  icon,
  label,
  value,
  muted = false,
}: {
  icon: ReactNode;
  label: ReactNode;
  value: string;
  muted?: boolean;
}) {
  const valueClass = muted
    ? "mt-1 break-words whitespace-pre-wrap font-mono text-sm text-slate-400"
    : "mt-1 break-words whitespace-pre-wrap font-mono text-sm text-slate-900";

  return (
    <div className="min-w-0 rounded-md border border-white/80 bg-white px-3 py-2">
      <div className="flex min-w-0 items-center gap-2 text-xs font-medium text-slate-500">
        <span className="shrink-0">{icon}</span>
        <span className="min-w-0 break-words">{label}</span>
      </div>
      <div className={valueClass}>{value}</div>
    </div>
  );
}

function EcdhChannel({
  stage,
  alicePublic,
  bobPublic,
}: {
  stage: EcdhStage;
  alicePublic: AffinePoint;
  bobPublic: AffinePoint;
}) {
  const exchanged = hasReached(stage, "exchanged");
  const shared = hasReached(stage, "shared");
  const status = shared
    ? "Secreto listo"
    : exchanged
      ? "Públicas en destino"
      : hasReached(stage, "public")
        ? "Listo para enviar"
        : "En espera";

  return (
    <div className="grid min-w-0 gap-3 rounded-md border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <ArrowRightLeft className="h-4 w-4 text-indigo-700" aria-hidden="true" />
          <h3 className="text-sm font-semibold text-slate-950">Canal público</h3>
        </div>
        <span
          className={
            shared
              ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-800"
              : exchanged
                ? "rounded-full bg-indigo-100 px-2 py-1 text-xs font-medium text-indigo-800"
                : "rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600"
          }
        >
          {status}
        </span>
      </div>

      <div className="grid gap-2 rounded-md border border-dashed border-slate-300 bg-slate-50 px-3 py-4">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span>Alice</span>
          <span>Bob</span>
        </div>
        <div className="relative h-12 overflow-hidden rounded-md bg-white">
          <div className="absolute left-3 right-3 top-1/2 h-px bg-slate-300" />
          <span
            className={
              exchanged
                ? "absolute left-[55%] top-1/2 -translate-y-1/2 rounded bg-indigo-700 px-2 py-1 font-mono text-xs text-white transition-all"
                : "absolute left-3 top-1/2 -translate-y-1/2 rounded bg-slate-300 px-2 py-1 font-mono text-xs text-slate-600 transition-all"
            }
          >
            <MathTerm math="Q_A" />
          </span>
          <span
            className={
              exchanged
                ? "absolute right-[55%] top-1/2 -translate-y-1/2 rounded bg-amber-700 px-2 py-1 font-mono text-xs text-white transition-all"
                : "absolute right-3 top-1/2 -translate-y-1/2 rounded bg-slate-300 px-2 py-1 font-mono text-xs text-slate-600 transition-all"
            }
          >
            <MathTerm math="Q_B" />
          </span>
        </div>
      </div>

      <div className="rounded-md border border-slate-200 bg-slate-50 px-3 py-3">
        <div className="flex items-center gap-2 text-xs font-medium uppercase text-slate-500">
          <Eye className="h-4 w-4" aria-hidden="true" />
          Vista de Eve
        </div>
        <div className="mt-2 grid gap-1 font-mono text-xs text-slate-700">
          <span><MathTerm math="Q_A" /> = {exchanged ? formatPoint(alicePublic) : "pendiente"}</span>
          <span><MathTerm math="Q_B" /> = {exchanged ? formatPoint(bobPublic) : "pendiente"}</span>
          <span className="text-slate-500">S no viaja por el canal.</span>
        </div>
      </div>
    </div>
  );
}

function EcdhSharedSecretPanel({
  stage,
  aliceFormula,
  aliceSecret,
  bobFormula,
  bobSecret,
  matches,
  order,
}: {
  stage: EcdhStage;
  aliceFormula: ReactNode;
  aliceSecret: string;
  bobFormula: ReactNode;
  bobSecret: string;
  matches: boolean;
  order: number;
}) {
  if (!hasReached(stage, "shared")) {
    return (
      <div className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
        {hasReached(stage, "exchanged")
          ? "Las claves públicas ya están intercambiadas. El siguiente paso deriva el secreto local en cada extremo."
          : <>Cuando <MathTerm math="Q_A" /> y <MathTerm math="Q_B" /> viajen por el canal, cada extremo podrá calcular el mismo punto secreto sin enviarlo.</>}
      </div>
    );
  }

  return (
    <div
      className={
        matches
          ? "grid gap-4 rounded-md border border-emerald-200 bg-emerald-50 p-4"
          : "grid gap-4 rounded-md border border-rose-200 bg-rose-50 p-4"
      }
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <ShieldCheck
            className={matches ? "h-5 w-5 text-emerald-700" : "h-5 w-5 text-rose-700"}
            aria-hidden="true"
          />
          <h3 className="text-sm font-semibold text-slate-950">Secreto compartido</h3>
        </div>
        <span
          className={
            matches
              ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-800"
              : "rounded-full bg-rose-100 px-2 py-1 text-xs font-medium text-rose-800"
          }
        >
          {matches ? "Coinciden" : "No coinciden"}
        </span>
      </div>
      <div className="grid gap-3 lg:grid-cols-2">
        <div className="rounded-md border border-white/80 bg-white px-3 py-3">
          <div className="text-xs font-medium uppercase text-slate-500">Alice calcula</div>
          <div className="mt-2 font-mono text-xs text-slate-600">{aliceFormula}</div>
          <div className="mt-1 font-mono text-sm text-slate-950">{aliceSecret}</div>
        </div>
        <div className="rounded-md border border-white/80 bg-white px-3 py-3">
          <div className="text-xs font-medium uppercase text-slate-500">Bob calcula</div>
          <div className="mt-2 font-mono text-xs text-slate-600">{bobFormula}</div>
          <div className="mt-1 font-mono text-sm text-slate-950">{bobSecret}</div>
        </div>
      </div>
      <div className="rounded-md border border-white/80 bg-white px-3 py-2 text-sm text-slate-700">
        Orden de G: <span className="font-mono text-slate-950">{order}</span>
      </div>
    </div>
  );
}

function EcdsaTimeline({ stage }: { stage: EcdsaStage }) {
  const steps: Array<{ label: string; target: EcdsaStage }> = [
    { label: "Firmar localmente", target: "signed" },
    { label: "Publicar M, Q, (r, s)", target: "published" },
    { label: "Verificar con Q", target: "verified" },
  ];

  return (
    <div className="grid gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-3 sm:grid-cols-3">
      {steps.map((step) => {
        const done = hasReachedEcdsa(stage, step.target);
        const current = ecdsaStageRank[stage] + 1 === ecdsaStageRank[step.target];

        return (
          <div
            key={step.target}
            className={
              done
                ? "flex items-center gap-2 text-sm font-medium text-emerald-700"
                : current
                  ? "flex items-center gap-2 text-sm font-medium text-indigo-800"
                  : "flex items-center gap-2 text-sm font-medium text-slate-500"
            }
          >
            <span
              className={
                done
                  ? "flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100"
                  : current
                    ? "flex h-6 w-6 items-center justify-center rounded-full bg-indigo-100"
                    : "flex h-6 w-6 items-center justify-center rounded-full bg-white"
              }
            >
              {done ? <CheckCircle2 className="h-4 w-4" /> : ecdsaStageRank[step.target]}
            </span>
            {step.label}
          </div>
        );
      })}
    </div>
  );
}

function EcdsaSignerCard({
  stage,
  privateKey,
  nonce,
  publicKey,
  hash,
  signature,
}: {
  stage: EcdsaStage;
  privateKey: number;
  nonce: number;
  publicKey: AffinePoint;
  hash: number;
  signature: { r: number; s: number };
}) {
  const signed = hasReachedEcdsa(stage, "signed");

  return (
    <div className="grid min-w-0 gap-3 rounded-md border border-indigo-200 bg-indigo-50/60 p-4">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-indigo-700 text-white">
          <UserRound className="h-5 w-5" aria-hidden="true" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-950">Firmante</h3>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            Calcula la firma con la clave privada y un nonce de un solo uso.
          </p>
        </div>
      </div>

      <ProtocolValueBox
        icon={<Lock className="h-4 w-4" aria-hidden="true" />}
        label="Clave privada d"
        value={privateKey.toString()}
      />
      <ProtocolValueBox
        icon={<KeyRound className="h-4 w-4" aria-hidden="true" />}
        label="Nonce k"
        value={signed ? nonce.toString() : "pendiente"}
        muted={!signed}
      />
      <ProtocolValueBox
        icon={<Unlock className="h-4 w-4" aria-hidden="true" />}
        label="Q = dG"
        value={signed ? formatPoint(publicKey) : "pendiente"}
        muted={!signed}
      />
      <ProtocolValueBox
        icon={<Eye className="h-4 w-4" aria-hidden="true" />}
        label="H(m)"
        value={signed ? hash.toString() : "pendiente"}
        muted={!signed}
      />

      <div className="rounded-md border border-white/80 bg-white/75 px-3 py-2">
        <p className="font-mono text-xs leading-5 text-slate-700">
          {signed
            ? `firma = (r, s) = ${formatSignature(signature)}`
            : "La firma (r, s) se calcula localmente; d y k no se publican."}
        </p>
      </div>
    </div>
  );
}

function EcdsaPackageCard({
  stage,
  message,
  publicKey,
  signature,
}: {
  stage: EcdsaStage;
  message: string;
  publicKey: AffinePoint;
  signature: { r: number; s: number };
}) {
  const signed = hasReachedEcdsa(stage, "signed");
  const published = hasReachedEcdsa(stage, "published");
  const visibleMessage = message.length > 0 ? message : "(mensaje vacio)";
  const status = published ? "Publicado" : signed ? "Preparado" : "Sin firma";

  return (
    <div className="grid min-w-0 gap-3 rounded-md border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Send className="h-4 w-4 text-indigo-700" aria-hidden="true" />
          <h3 className="text-sm font-semibold text-slate-950">Paquete público</h3>
        </div>
        <span
          className={
            published
              ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-800"
              : signed
                ? "rounded-full bg-indigo-100 px-2 py-1 text-xs font-medium text-indigo-800"
                : "rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600"
          }
        >
          {status}
        </span>
      </div>

      <div className="rounded-md border border-dashed border-slate-300 bg-slate-50 px-3 py-3 text-xs leading-5 text-slate-600">
        {published
          ? "Viajan el mensaje, la clave pública y la firma. La clave privada y el nonce se quedan en el firmante."
          : signed
            ? "La firma ya existe, pero aún no se ha enviado al verificador."
            : "Primero se genera la firma con d, k y H(m)."}
      </div>

      <ProtocolValueBox
        icon={<Send className="h-4 w-4" aria-hidden="true" />}
        label="Mensaje M"
        value={published ? visibleMessage : "pendiente"}
        muted={!published}
      />
      <ProtocolValueBox
        icon={<Unlock className="h-4 w-4" aria-hidden="true" />}
        label="Clave pública Q"
        value={published ? formatPoint(publicKey) : "pendiente"}
        muted={!published}
      />
      <ProtocolValueBox
        icon={<ShieldCheck className="h-4 w-4" aria-hidden="true" />}
        label="Firma (r, s)"
        value={published ? formatSignature(signature) : "pendiente"}
        muted={!published}
      />
    </div>
  );
}

function EcdsaVerifierCard({
  stage,
  order,
  hash,
  signature,
  verification,
}: {
  stage: EcdsaStage;
  order: number;
  hash: number;
  signature: { r: number; s: number };
  verification: { u1: number; u2: number; point: AffinePoint; valid: boolean };
}) {
  const published = hasReachedEcdsa(stage, "published");
  const verified = hasReachedEcdsa(stage, "verified");

  return (
    <div className="grid min-w-0 gap-3 rounded-md border border-emerald-200 bg-emerald-50/60 p-4">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-emerald-700 text-white">
          <ShieldCheck className="h-5 w-5" aria-hidden="true" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-950">Verificador</h3>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            Usa solo datos públicos para reconstruir un punto de control.
          </p>
        </div>
      </div>

      <ProtocolValueBox
        icon={<Eye className="h-4 w-4" aria-hidden="true" />}
        label="Datos recibidos"
        value={published ? "M, Q, (r, s)" : "pendiente"}
        muted={!published}
      />
      <ProtocolValueBox
        icon={<KeyRound className="h-4 w-4" aria-hidden="true" />}
        label="u₁ = H(m)s⁻¹"
        value={verified ? verification.u1.toString() : "pendiente"}
        muted={!verified}
      />
      <ProtocolValueBox
        icon={<KeyRound className="h-4 w-4" aria-hidden="true" />}
        label="u₂ = rs⁻¹"
        value={verified ? verification.u2.toString() : "pendiente"}
        muted={!verified}
      />
      <ProtocolValueBox
        icon={<CheckCircle2 className="h-4 w-4" aria-hidden="true" />}
        label="R' = u₁G + u₂Q"
        value={verified ? formatPoint(verification.point) : "pendiente"}
        muted={!verified}
      />

      <div className="rounded-md border border-white/80 bg-white/75 px-3 py-2">
        <p className="font-mono text-xs leading-5 text-slate-700">
          {verified
            ? `x(R') (mod ${order}) debe ser r = ${signature.r}`
            : `n = ${order}, H(m) = ${hash}, r = ${signature.r}, s = ${signature.s}`}
        </p>
      </div>
    </div>
  );
}

function EcdsaVerificationPanel({
  stage,
  order,
  signature,
  verification,
}: {
  stage: EcdsaStage;
  order: number;
  signature: { r: number; s: number };
  verification: { u1: number; u2: number; point: AffinePoint; valid: boolean };
}) {
  if (!hasReachedEcdsa(stage, "verified")) {
    return (
      <div className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
        {hasReachedEcdsa(stage, "published")
          ? "El paquete público ya está disponible. La verificación recomputa R' = u₁G + u₂Q y compara su coordenada x con r."
          : "La firma ECDSA se acepta solo si el verificador puede reconstruir un punto cuya x módulo n coincide con r."}
      </div>
    );
  }

  const xResidue =
    verification.point.x === null ? "𝒪" : (verification.point.x % order).toString();

  return (
    <div
      className={
        verification.valid
          ? "grid gap-4 rounded-md border border-emerald-200 bg-emerald-50 p-4"
          : "grid gap-4 rounded-md border border-rose-200 bg-rose-50 p-4"
      }
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <CheckCircle2
            className={verification.valid ? "h-5 w-5 text-emerald-700" : "h-5 w-5 text-rose-700"}
            aria-hidden="true"
          />
          <h3 className="text-sm font-semibold text-slate-950">
            {verification.valid ? "Firma válida" : "Firma no válida"}
          </h3>
        </div>
        <span
          className={
            verification.valid
              ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-800"
              : "rounded-full bg-rose-100 px-2 py-1 text-xs font-medium text-rose-800"
          }
        >
          n = {order}
        </span>
      </div>
      <div className="grid gap-3 lg:grid-cols-2">
        <div className="rounded-md border border-white/80 bg-white px-3 py-3">
          <div className="text-xs font-medium uppercase text-slate-500">Reconstrucción</div>
          <div className="mt-2 font-mono text-xs text-slate-600">
            R' = {verification.u1}G + {verification.u2}Q
          </div>
          <div className="mt-1 font-mono text-sm text-slate-950">{formatPoint(verification.point)}</div>
        </div>
        <div className="rounded-md border border-white/80 bg-white px-3 py-3">
          <div className="text-xs font-medium uppercase text-slate-500">Comparación</div>
          <div className="mt-2 font-mono text-xs text-slate-600">x(R') (mod n) = {xResidue}</div>
          <div className="mt-1 font-mono text-sm text-slate-950">r = {signature.r}</div>
        </div>
      </div>
    </div>
  );
}

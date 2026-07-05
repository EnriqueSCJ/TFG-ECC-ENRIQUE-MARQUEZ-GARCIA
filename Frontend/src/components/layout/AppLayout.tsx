import type { ReactNode } from "react";
import { ErrorBanner } from "../common/ErrorBanner";
import { Sidebar } from "./Sidebar";
import { useCurveStore } from "../../store/curveStore";

interface AppLayoutProps {
  children: ReactNode;
}

const moduleTitles = {
  "learning-path": "Ruta visual de ECC",
  weierstrass: "Exploración de Weierstrass",
  "group-law": "Ley de Grupo",
  "finite-fields": "Cuerpos finitos 𝔽ₚ",
  ecdlp: "Logaritmo Discreto ECDLP",
  protocols: "Protocolos ECC",
  "audit-attacks": "Auditoría y ataques",
};

export function AppLayout({ children }: AppLayoutProps) {
  const activeModule = useCurveStore((state) => state.activeModule);
  const setActiveModule = useCurveStore((state) => state.setActiveModule);
  const apiError = useCurveStore((state) => state.apiError);
  const setApiError = useCurveStore((state) => state.setApiError);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[18rem_1fr]">
        <Sidebar activeModule={activeModule} onSelect={setActiveModule} />
        <main className="min-w-0 bg-slate-100">
          <div className="mx-auto flex w-full max-w-7xl flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
            <header className="flex flex-col gap-2 border-b border-slate-300 pb-4">
              <span className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                Cuaderno interactivo
              </span>
              <h1 className="text-2xl font-semibold text-slate-950">
                {moduleTitles[activeModule]}
              </h1>
            </header>

            {apiError ? (
              <ErrorBanner
                title="Respuesta del backend"
                message={apiError}
                onDismiss={() => setApiError(null)}
              />
            ) : null}

            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

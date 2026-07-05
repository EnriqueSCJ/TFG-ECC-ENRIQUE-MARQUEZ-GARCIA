import {
  Atom,
  BookOpen,
  GitBranch,
  Hash,
  KeyRound,
  LineChart,
  Radar,
  ShieldAlert,
} from "lucide-react";
import { cn } from "../../lib/styles";
import { ModuleId } from "../../types/ecc";

interface SidebarProps {
  activeModule: ModuleId;
  onSelect: (moduleId: ModuleId) => void;
}

const navigation: Array<{
  id: ModuleId;
  label: string;
  subtitle: string;
  icon: typeof LineChart;
}> = [
  {
    id: "learning-path",
    label: "Ruta ECC",
    subtitle: "Vídeos",
    icon: BookOpen,
  },
  {
    id: "weierstrass",
    label: "Módulo 1",
    subtitle: "Weierstrass",
    icon: LineChart,
  },
  {
    id: "group-law",
    label: "Módulo 2",
    subtitle: "Ley de Grupo",
    icon: GitBranch,
  },
  {
    id: "finite-fields",
    label: "Módulo 3",
    subtitle: "Cuerpos finitos 𝔽ₚ",
    icon: Hash,
  },
  {
    id: "ecdlp",
    label: "Módulo 4",
    subtitle: "ECDLP",
    icon: KeyRound,
  },
  {
    id: "protocols",
    label: "Módulo 5",
    subtitle: "Protocolos",
    icon: ShieldAlert,
  },
  {
    id: "audit-attacks",
    label: "Auditoría",
    subtitle: "Ataques",
    icon: Radar,
  },
];

export function Sidebar({ activeModule, onSelect }: SidebarProps) {
  return (
    <aside className="flex h-full w-full flex-col border-r border-slate-200 bg-white px-4 py-5 lg:sticky lg:top-0 lg:h-screen lg:w-72 lg:overflow-y-auto">
      <div className="mb-6 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 bg-slate-50 text-indigo-800">
          <Atom className="h-5 w-5" aria-hidden="true" />
        </div>
        <div>
          <h1 className="text-xl font-semibold tracking-tight text-slate-950">ECC Lab</h1>
        </div>
      </div>

      <nav className="grid gap-1.5">
        {navigation.map((item) => {
          const Icon = item.icon;
          const active = activeModule === item.id;

          return (
            <button
              key={item.id}
              type="button"
              onClick={() => onSelect(item.id)}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-3 text-left transition",
                active
                  ? "border border-indigo-200 bg-indigo-50 text-indigo-950"
                  : "border border-transparent text-slate-600 hover:border-slate-200 hover:bg-slate-50 hover:text-slate-950",
              )}
            >
              <Icon className="h-5 w-5 shrink-0" aria-hidden="true" />
              <span className="min-w-0">
                <span className="block text-xs uppercase tracking-[0.14em]">{item.label}</span>
                <span className="block truncate text-sm font-medium">{item.subtitle}</span>
              </span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

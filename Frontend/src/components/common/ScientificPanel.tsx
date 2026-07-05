import type { ReactNode } from "react";

interface ScientificPanelProps {
  title: ReactNode;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
}

export function ScientificPanel({ title, description, action, children }: ScientificPanelProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-5 flex flex-col gap-3 border-b border-slate-200 pb-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
          {description ? <p className="mt-1 max-w-3xl text-sm text-slate-600">{description}</p> : null}
        </div>
        {action ? <div className="shrink-0">{action}</div> : null}
      </div>
      {children}
    </section>
  );
}

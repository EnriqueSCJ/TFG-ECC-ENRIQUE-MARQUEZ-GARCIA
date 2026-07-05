import { AlertTriangle, X } from "lucide-react";

interface ErrorBannerProps {
  title?: string;
  message: string;
  onDismiss?: () => void;
}

export function ErrorBanner({ title = "Error", message, onDismiss }: ErrorBannerProps) {
  return (
    <div className="flex items-start gap-3 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-950">
      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-rose-700" aria-hidden="true" />
      <div className="min-w-0 flex-1">
        <p className="font-semibold text-rose-950">{title}</p>
        <p className="mt-1 text-rose-800">{message}</p>
      </div>
      {onDismiss ? (
        <button
          type="button"
          onClick={onDismiss}
          className="rounded-md p-1 text-rose-700 transition hover:bg-rose-100 hover:text-rose-950"
          aria-label="Cerrar error"
          title="Cerrar error"
        >
          <X className="h-4 w-4" aria-hidden="true" />
        </button>
      ) : null}
    </div>
  );
}

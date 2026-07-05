import { Info } from "lucide-react";
import { useEffect, useId, useRef, useState, type ReactNode } from "react";

interface ConceptHintProps {
  children: ReactNode;
  title: string;
  description: string;
}

export function ConceptHint({ children, title, description }: ConceptHintProps) {
  const [open, setOpen] = useState(false);
  const id = useId();
  const wrapperRef = useRef<HTMLSpanElement | null>(null);

  useEffect(() => {
    if (!open) return;

    const closeOnOutsideClick = (event: MouseEvent) => {
      if (!wrapperRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };

    document.addEventListener("mousedown", closeOnOutsideClick);
    document.addEventListener("keydown", closeOnEscape);

    return () => {
      document.removeEventListener("mousedown", closeOnOutsideClick);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [open]);

  return (
    <span ref={wrapperRef} className="relative inline-flex items-center">
      <button
        type="button"
        aria-expanded={open}
        aria-describedby={open ? id : undefined}
        onClick={() => setOpen((value) => !value)}
        className="inline-flex items-center gap-1 rounded-sm border-b border-dotted border-indigo-300 text-slate-700 normal-case outline-none transition hover:border-indigo-600 hover:text-indigo-800 focus-visible:ring-2 focus-visible:ring-indigo-200"
      >
        <Info className="h-3.5 w-3.5 text-indigo-700" aria-hidden="true" />
        <span>{children}</span>
      </button>

      {open ? (
        <span
          id={id}
          role="tooltip"
          className="absolute left-0 top-full z-20 mt-2 w-80 rounded-md border border-slate-200 bg-white px-3.5 py-3 text-left text-sm normal-case leading-6 text-slate-600 shadow-lg"
        >
          <span className="block font-semibold text-slate-950">{title}</span>
          <span className="mt-1 block">{description}</span>
        </span>
      ) : null}
    </span>
  );
}

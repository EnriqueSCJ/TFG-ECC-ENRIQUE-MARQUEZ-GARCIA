import { useEffect, useState } from "react";
import { BookOpen, CheckCircle2, ChevronLeft, ChevronRight, PlayCircle } from "lucide-react";
import { ScientificPanel } from "../components/common/ScientificPanel";
import { cn } from "../lib/styles";
import { useCurveStore } from "../store/curveStore";
import type { ModuleId } from "../types/ecc";

const STORAGE_KEY = "ecc-learning-path-watched";

interface CourseVideo {
  id: string;
  number: number;
  title: string;
  stage: string;
  focus: string;
  source: string;
  relatedModule?: {
    id: ModuleId;
    label: string;
  };
}

const COURSE_VIDEOS: CourseVideo[] = [
  {
    id: "que-es-una-curva-eliptica",
    number: 1,
    title: "Qué es una curva elíptica",
    stage: "Fundamentos",
    focus: "La forma geométrica de la curva y por qué aparece la ecuación de Weierstrass.",
    source: "/videos/ecc/01-que-es-una-curva-eliptica.mp4",
    relatedModule: { id: "weierstrass", label: "Explorar Weierstrass" },
  },
  {
    id: "ley-de-grupo",
    number: 2,
    title: "Ley de grupo",
    stage: "Fundamentos",
    focus: "La suma de puntos como operación algebraica y visual.",
    source: "/videos/ecc/02-ley-de-grupo.mp4",
    relatedModule: { id: "group-law", label: "Probar la suma" },
  },
  {
    id: "casos-especiales",
    number: 3,
    title: "Casos especiales",
    stage: "Fundamentos",
    focus: "Tangentes, punto del infinito y situaciones límite de la suma.",
    source: "/videos/ecc/03-casos-especiales.mp4",
    relatedModule: { id: "group-law", label: "Ver la geometría" },
  },
  {
    id: "campos-finitos",
    number: 4,
    title: "Campos finitos",
    stage: "Aritmética discreta",
    focus: "Cómo se pasa de curvas reales a puntos sobre un cuerpo primo.",
    source: "/videos/ecc/04-campos-finitos.mp4",
    relatedModule: { id: "finite-fields", label: "Ver puntos en 𝔽ₚ" },
  },
  {
    id: "multiplicacion-escalar",
    number: 5,
    title: "Multiplicación escalar",
    stage: "Aritmética discreta",
    focus: "La operación kG como repetición eficiente de la ley de grupo.",
    source: "/videos/ecc/05-multiplicacion-escalar.mp4",
    relatedModule: { id: "ecdlp", label: "Recorrer kG" },
  },
  {
    id: "logaritmo-discreto",
    number: 6,
    title: "Logaritmo discreto",
    stage: "Seguridad",
    focus: "El problema ECDLP y por qué sostiene la seguridad de ECC.",
    source: "/videos/ecc/06-logaritmo-discreto.mp4",
    relatedModule: { id: "ecdlp", label: "Abrir ECDLP" },
  },
  {
    id: "ecdh",
    number: 7,
    title: "ECDH",
    stage: "Protocolos",
    focus: "Intercambio de claves mediante secretos privados y puntos públicos.",
    source: "/videos/ecc/07-ecdh.mp4",
    relatedModule: { id: "protocols", label: "Simular ECDH" },
  },
  {
    id: "ecdsa",
    number: 8,
    title: "ECDSA",
    stage: "Protocolos",
    focus: "Firmas digitales con nonce, par de claves y verificación pública.",
    source: "/videos/ecc/08-ecdsa.mp4",
    relatedModule: { id: "protocols", label: "Simular ECDSA" },
  },
  {
    id: "ataque-pollards-rho",
    number: 9,
    title: "Ataque de Pollard ρ",
    stage: "Ataques",
    focus: "Búsqueda de colisiones para resolver el logaritmo discreto en grupos pequeños.",
    source: "/videos/ecc/09-ataque-pollards-rho.mp4",
    relatedModule: { id: "audit-attacks", label: "Auditar ataques" },
  },
  {
    id: "curvas-anomalas",
    number: 10,
    title: "Curvas anómalas",
    stage: "Ataques",
    focus: "El caso #E(𝔽ₚ) = p y por qué es una señal crítica en una auditoría.",
    source: "/videos/ecc/10-curvas-anomalas.mp4",
    relatedModule: { id: "audit-attacks", label: "Revisar anomalías" },
  },
  {
    id: "ataque-smart",
    number: 11,
    title: "Ataque de Smart",
    stage: "Ataques",
    focus: "La reducción que vuelve peligrosas ciertas curvas anómalas.",
    source: "/videos/ecc/11-ataque-smart.mp4",
    relatedModule: { id: "audit-attacks", label: "Ver criterio Smart" },
  },
  {
    id: "canal-lateral-energia",
    number: 12,
    title: "Canales laterales",
    stage: "Implementación",
    focus: "Riesgos de energía, tiempo y trazas físicas en implementaciones reales.",
    source: "/videos/ecc/12-canal-lateral-energia.mp4",
  },
  {
    id: "curvas-montgomery-edwards",
    number: 13,
    title: "Curvas Montgomery y Edwards",
    stage: "Implementación",
    focus: "Modelos alternativos usados para fórmulas rápidas y seguras.",
    source: "/videos/ecc/13-curvas-montgomery-edwards.mp4",
  },
  {
    id: "pairings-bilineales",
    number: 14,
    title: "Pairings bilineales",
    stage: "Extensiones",
    focus: "Aplicaciones donde se aprovechan emparejamientos entre grupos.",
    source: "/videos/ecc/14-pairings-bilineales.mp4",
  },
  {
    id: "zksnarks",
    number: 15,
    title: "zk-SNARKs",
    stage: "Extensiones",
    focus: "Pruebas de conocimiento cero apoyadas en estructuras algebraicas.",
    source: "/videos/ecc/15-zksnarks.mp4",
  },
  {
    id: "algoritmo-de-shor",
    number: 16,
    title: "Algoritmo de Shor",
    stage: "Horizonte cuántico",
    focus: "Por qué un ordenador cuántico cambiaría el panorama del logaritmo discreto.",
    source: "/videos/ecc/16-algoritmo-de-shor.mp4",
  },
  {
    id: "criptografia-de-isogenias",
    number: 17,
    title: "Criptografía de isogenias",
    stage: "Postcuántica",
    focus: "La idea de moverse entre curvas mediante mapas algebraicos.",
    source: "/videos/ecc/17-criptografia-de-isogenias.mp4",
  },
  {
    id: "grafo-del-multiverso",
    number: 18,
    title: "Grafo del multiverso",
    stage: "Postcuántica",
    focus: "Visualización de familias de curvas conectadas por isogenias.",
    source: "/videos/ecc/18-grafo-del-multiverso.mp4",
  },
  {
    id: "ataque-asidh",
    number: 19,
    title: "Ataque a SIDH",
    stage: "Postcuántica",
    focus: "Cómo una construcción prometedora terminó rota por un ataque estructural.",
    source: "/videos/ecc/19-ataque-asidh.mp4",
  },
  {
    id: "protocolos-modernos-ecc",
    number: 20,
    title: "Protocolos modernos ECC",
    stage: "Cierre",
    focus: "Panorama final de usos, límites y buenas prácticas.",
    source: "/videos/ecc/20-protocolos-modernos-ecc.mp4",
    relatedModule: { id: "protocols", label: "Volver a protocolos" },
  },
];

function readWatchedVideos(): Set<string> {
  if (typeof window === "undefined") return new Set();

  try {
    const rawValue = window.localStorage.getItem(STORAGE_KEY);
    const parsedValue = rawValue ? JSON.parse(rawValue) : [];
    return new Set(Array.isArray(parsedValue) ? parsedValue : []);
  } catch {
    return new Set();
  }
}

export function LearningPathView() {
  const setActiveModule = useCurveStore((state) => state.setActiveModule);
  const [activeVideoId, setActiveVideoId] = useState(COURSE_VIDEOS[0].id);
  const [watchedVideos, setWatchedVideos] = useState<Set<string>>(readWatchedVideos);

  const activeIndex = COURSE_VIDEOS.findIndex((video) => video.id === activeVideoId);
  const activeVideo = COURSE_VIDEOS[activeIndex] ?? COURSE_VIDEOS[0];
  const previousVideo = activeIndex > 0 ? COURSE_VIDEOS[activeIndex - 1] : null;
  const nextVideo = activeIndex < COURSE_VIDEOS.length - 1 ? COURSE_VIDEOS[activeIndex + 1] : null;
  const progressPercent = Math.round((watchedVideos.size / COURSE_VIDEOS.length) * 100);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(watchedVideos)));
  }, [watchedVideos]);

  const toggleWatched = (videoId: string) => {
    setWatchedVideos((current) => {
      const next = new Set(current);
      if (next.has(videoId)) {
        next.delete(videoId);
      } else {
        next.add(videoId);
      }
      return next;
    });
  };

  return (
    <div className="grid items-start gap-5 xl:grid-cols-[1fr_24rem]">
      <ScientificPanel
        title={activeVideo.title}
        description={`Capítulo ${String(activeVideo.number).padStart(2, "0")} · ${activeVideo.stage}`}
        action={
          <button
            type="button"
            onClick={() => toggleWatched(activeVideo.id)}
            className={cn(
              "inline-flex items-center gap-2 rounded-md border px-3 py-2 text-sm font-medium transition",
              watchedVideos.has(activeVideo.id)
                ? "border-emerald-200 bg-emerald-50 text-emerald-800"
                : "border-slate-300 bg-white text-slate-700 hover:bg-slate-50",
            )}
          >
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
            {watchedVideos.has(activeVideo.id) ? "Visto" : "Marcar visto"}
          </button>
        }
      >
        <div className="grid gap-5">
          <div className="overflow-hidden rounded-lg border border-slate-900 bg-slate-950 shadow-sm">
            <video
              key={activeVideo.id}
              className="aspect-video w-full bg-slate-950"
              controls
              preload="metadata"
              src={activeVideo.source}
            >
              Tu navegador no puede reproducir este vídeo.
            </video>
          </div>

          <div className="grid gap-3 lg:grid-cols-[1fr_auto] lg:items-center">
            <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-start gap-3">
                <BookOpen className="mt-0.5 h-5 w-5 shrink-0 text-indigo-700" aria-hidden="true" />
                <div>
                  <h3 className="text-sm font-semibold text-slate-950">Idea clave</h3>
                  <p className="mt-1 text-sm leading-6 text-slate-600">{activeVideo.focus}</p>
                </div>
              </div>
            </div>

            {activeVideo.relatedModule ? (
              <button
                type="button"
                onClick={() => setActiveModule(activeVideo.relatedModule!.id)}
                className="inline-flex h-11 items-center justify-center rounded-md border border-indigo-200 bg-indigo-50 px-4 text-sm font-semibold text-indigo-900 transition hover:bg-indigo-100"
              >
                {activeVideo.relatedModule.label}
              </button>
            ) : null}
          </div>

          <div className="flex flex-col gap-3 border-t border-slate-200 pt-4 sm:flex-row sm:items-center sm:justify-between">
            <button
              type="button"
              disabled={!previousVideo}
              onClick={() => previousVideo && setActiveVideoId(previousVideo.id)}
              className="inline-flex items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              <ChevronLeft className="h-4 w-4" aria-hidden="true" />
              Anterior
            </button>
            <span className="text-center font-mono text-xs text-slate-500">
              {activeIndex + 1} / {COURSE_VIDEOS.length}
            </span>
            <button
              type="button"
              disabled={!nextVideo}
              onClick={() => nextVideo && setActiveVideoId(nextVideo.id)}
              className="inline-flex items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Siguiente
              <ChevronRight className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </ScientificPanel>

      <ScientificPanel
        title="Ruta de vídeos"
        description="Secuencia ordenada para recorrer ECC de principio a fin."
      >
        <div className="grid gap-4">
          <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
            <div className="flex items-center justify-between gap-3 text-sm">
              <span className="font-medium text-slate-800">Progreso</span>
              <span className="font-mono text-slate-700">
                {watchedVideos.size}/{COURSE_VIDEOS.length}
              </span>
            </div>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200">
              <div
                className="h-full rounded-full bg-indigo-700 transition-all"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div className="grid max-h-[38rem] gap-2 overflow-y-auto pr-1">
            {COURSE_VIDEOS.map((video) => {
              const active = video.id === activeVideo.id;
              const watched = watchedVideos.has(video.id);

              return (
                <button
                  key={video.id}
                  type="button"
                  onClick={() => setActiveVideoId(video.id)}
                  className={cn(
                    "grid grid-cols-[2.25rem_1fr_auto] items-center gap-3 rounded-md border px-3 py-2.5 text-left transition",
                    active
                      ? "border-indigo-200 bg-indigo-50 text-indigo-950"
                      : "border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50",
                  )}
                >
                  <span
                    className={cn(
                      "flex h-8 w-8 items-center justify-center rounded-md border font-mono text-xs",
                      active
                        ? "border-indigo-200 bg-white text-indigo-900"
                        : "border-slate-200 bg-slate-50 text-slate-600",
                    )}
                  >
                    {String(video.number).padStart(2, "0")}
                  </span>
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-semibold">{video.title}</span>
                    <span className="block truncate text-xs text-slate-500">{video.stage}</span>
                  </span>
                  {watched ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-600" aria-label="Visto" />
                  ) : (
                    <PlayCircle className="h-4 w-4 text-slate-400" aria-hidden="true" />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </ScientificPanel>
    </div>
  );
}

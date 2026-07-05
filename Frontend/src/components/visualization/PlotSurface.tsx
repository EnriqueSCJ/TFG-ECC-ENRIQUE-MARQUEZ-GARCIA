import Plotly from "plotly.js-dist-min";
import { memo, PointerEvent as ReactPointerEvent, useCallback, useMemo, useRef } from "react";
import createPlotlyComponent from "react-plotly.js/factory";

const Plot = createPlotlyComponent(Plotly);

type AxisRange = [number, number];
type PlotPoint = {
  x: number;
  y: number;
};
type PlotAxis = { range?: number[]; _length?: number };

interface PlotlyGraphDiv extends HTMLElement {
  _fullLayout?: {
    xaxis?: PlotAxis;
    yaxis?: PlotAxis;
    _size?: { w?: number; h?: number };
  };
}

interface DragState {
  pointerId: number;
  startClientX: number;
  startClientY: number;
  startXRange: AxisRange;
  startYRange: AxisRange;
  plotWidth: number;
  plotHeight: number;
}

interface PlotSurfaceProps {
  data: Array<Record<string, unknown>>;
  layout?: Record<string, unknown>;
  height?: number;
  maxZoomOutSteps?: number;
  panBounds?: {
    x?: AxisRange;
    y?: AxisRange;
  };
  fitPanYToVisibleData?: boolean;
}

const axisStyle = {
  automargin: true,
  gridcolor: "rgba(100, 116, 139, 0.2)",
  griddash: "dot",
  linecolor: "#94a3b8",
  mirror: false,
  showgrid: true,
  showline: true,
  tickcolor: "#94a3b8",
  tickfont: { color: "#475569", family: "JetBrains Mono, monospace", size: 11 },
  ticks: "outside",
  titlefont: { color: "#334155", family: "Inter, sans-serif", size: 12 },
  zerolinecolor: "#64748b",
  zerolinewidth: 1,
};

function asAxisRecord(axis: unknown): Record<string, unknown> {
  return axis && typeof axis === "object" ? (axis as Record<string, unknown>) : {};
}

function asAxisRange(value: unknown): AxisRange | null {
  if (!Array.isArray(value) || value.length !== 2) return null;
  const [start, end] = value.map(Number);
  return Number.isFinite(start) && Number.isFinite(end) ? [start, end] : null;
}

function rangeSpan(range: AxisRange): number {
  return range[1] - range[0];
}

function rangeCenter(range: AxisRange): number {
  return (range[0] + range[1]) / 2;
}

function clampRange(range: AxisRange, bounds: AxisRange): AxisRange {
  const span = rangeSpan(range);
  const boundsSpan = rangeSpan(bounds);

  if (span >= boundsSpan) {
    const center = (bounds[0] + bounds[1]) / 2;
    return [center - span / 2, center + span / 2];
  }

  let start = range[0];
  let end = range[1];

  if (start < bounds[0]) {
    end += bounds[0] - start;
    start = bounds[0];
  }

  if (end > bounds[1]) {
    start -= end - bounds[1];
    end = bounds[1];
  }

  return [Number(start.toFixed(6)), Number(end.toFixed(6))];
}

function limitRangeSpan(range: AxisRange, maxSpan: number): AxisRange {
  const span = rangeSpan(range);
  if (span <= maxSpan) return range;

  const center = rangeCenter(range);
  const halfSpan = maxSpan / 2;
  return [Number((center - halfSpan).toFixed(6)), Number((center + halfSpan).toFixed(6))];
}

function rangesMatch(left: AxisRange, right: AxisRange): boolean {
  return Math.abs(left[0] - right[0]) < 1e-6 && Math.abs(left[1] - right[1]) < 1e-6;
}

function rangeFromAxis(axis?: PlotAxis): AxisRange | null {
  if (!axis || typeof axis !== "object") return null;
  return asAxisRange(axis.range);
}

function numericCurvePoints(data: Array<Record<string, unknown>>): PlotPoint[] {
  const points: PlotPoint[] = [];

  data.forEach((trace) => {
    if (trace.connectgaps !== false || !Array.isArray(trace.x) || !Array.isArray(trace.y)) {
      return;
    }

    const xs = trace.x as unknown[];
    const ys = trace.y as unknown[];

    xs.forEach((rawX, index) => {
      const rawY = ys[index];
      const x = Number(rawX);
      const y = Number(rawY);

      if (Number.isFinite(x) && Number.isFinite(y)) {
        points.push({ x, y });
      }
    });
  });

  return points;
}

function visibleYBounds(points: PlotPoint[], xRange: AxisRange, fallback: AxisRange): AxisRange {
  let minY = Number.POSITIVE_INFINITY;
  let maxY = Number.NEGATIVE_INFINITY;

  points.forEach((point) => {
    if (point.x < xRange[0] || point.x > xRange[1]) return;
    minY = Math.min(minY, point.y);
    maxY = Math.max(maxY, point.y);
  });

  if (!Number.isFinite(minY) || !Number.isFinite(maxY)) {
    return fallback;
  }

  const padding = Math.max(0.6, (maxY - minY) * 0.08);
  return [minY - padding, maxY + padding];
}

function shouldStartCustomPan(target: EventTarget | null): boolean {
  return target instanceof Element && !target.closest(".modebar, button, a, input, select, textarea");
}

export const PlotSurface = memo(function PlotSurface({
  data,
  layout,
  height = 420,
  maxZoomOutSteps,
  panBounds,
  fitPanYToVisibleData = false,
}: PlotSurfaceProps) {
  const { xaxis, yaxis, ...restLayout } = layout ?? {};
  const xAxis = asAxisRecord(xaxis);
  const yAxis = asAxisRecord(yaxis);
  const initialXRange = asAxisRange(xAxis.range);
  const initialYRange = asAxisRange(yAxis.range);
  const maxZoomFactor = maxZoomOutSteps === undefined ? null : 2 ** maxZoomOutSteps;
  const graphRef = useRef<PlotlyGraphDiv | null>(null);
  const dragRef = useRef<DragState | null>(null);
  const nextRangeRef = useRef<{ x: AxisRange; y: AxisRange } | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const curvePointsRef = useRef<PlotPoint[]>([]);
  const curvePoints = useMemo(() => numericCurvePoints(data), [data]);
  curvePointsRef.current = curvePoints;

  const flushPan = useCallback(() => {
    animationFrameRef.current = null;
    const graphDiv = graphRef.current;
    const nextRange = nextRangeRef.current;

    if (!graphDiv || !nextRange) return;

    void Plotly.relayout(graphDiv as never, {
      "xaxis.range": nextRange.x,
      "yaxis.range": nextRange.y,
    } as never);
  }, []);

  const schedulePan = useCallback(
    (xRange: AxisRange, yRange: AxisRange) => {
      nextRangeRef.current = { x: xRange, y: yRange };

      if (animationFrameRef.current === null) {
        animationFrameRef.current = window.requestAnimationFrame(flushPan);
      }
    },
    [flushPan],
  );

  const handlePointerDown = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      if (!panBounds || event.button !== 0 || !shouldStartCustomPan(event.target)) return;

      const graphDiv = graphRef.current;
      const xRange = rangeFromAxis(graphDiv?._fullLayout?.xaxis) ?? asAxisRange(xAxis.range);
      const yRange = rangeFromAxis(graphDiv?._fullLayout?.yaxis) ?? asAxisRange(yAxis.range);

      if (!graphDiv || !xRange || !yRange) return;

      const plotWidth = graphDiv._fullLayout?.xaxis?._length ?? graphDiv._fullLayout?._size?.w;
      const plotHeight = graphDiv._fullLayout?.yaxis?._length ?? graphDiv._fullLayout?._size?.h;

      if (!plotWidth || !plotHeight) return;

      event.preventDefault();
      event.stopPropagation();
      event.currentTarget.setPointerCapture(event.pointerId);

      dragRef.current = {
        pointerId: event.pointerId,
        startClientX: event.clientX,
        startClientY: event.clientY,
        startXRange: xRange,
        startYRange: yRange,
        plotWidth,
        plotHeight,
      };
    },
    [panBounds, xAxis.range, yAxis.range],
  );

  const handlePointerMove = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      const drag = dragRef.current;
      if (!drag || drag.pointerId !== event.pointerId) return;

      event.preventDefault();
      event.stopPropagation();

      const xUnitsPerPixel = rangeSpan(drag.startXRange) / drag.plotWidth;
      const yUnitsPerPixel = rangeSpan(drag.startYRange) / drag.plotHeight;
      const deltaX = event.clientX - drag.startClientX;
      const deltaY = event.clientY - drag.startClientY;

      let nextXRange: AxisRange = [
        drag.startXRange[0] - deltaX * xUnitsPerPixel,
        drag.startXRange[1] - deltaX * xUnitsPerPixel,
      ];
      let nextYRange: AxisRange = [
        drag.startYRange[0] + deltaY * yUnitsPerPixel,
        drag.startYRange[1] + deltaY * yUnitsPerPixel,
      ];

      if (panBounds?.x) {
        nextXRange = clampRange(nextXRange, panBounds.x);
      }

      const yBounds = fitPanYToVisibleData
        ? visibleYBounds(curvePointsRef.current, nextXRange, panBounds?.y ?? drag.startYRange)
        : panBounds?.y;

      if (yBounds) {
        nextYRange = clampRange(nextYRange, yBounds);
      }

      schedulePan(nextXRange, nextYRange);
    },
    [fitPanYToVisibleData, panBounds, schedulePan],
  );

  const handlePointerUp = useCallback((event: ReactPointerEvent<HTMLDivElement>) => {
    if (dragRef.current?.pointerId !== event.pointerId) return;
    dragRef.current = null;
    event.currentTarget.releasePointerCapture(event.pointerId);
  }, []);

  const handleRelayout = useCallback(
    (event: Readonly<Record<string, unknown>>) => {
      if (!maxZoomFactor || !graphRef.current) return;

      let nextXRange = asAxisRange(event["xaxis.range"]);
      let nextYRange = asAxisRange(event["yaxis.range"]);

      if (!nextXRange) {
        const xStart = Number(event["xaxis.range[0]"]);
        const xEnd = Number(event["xaxis.range[1]"]);
        nextXRange =
          Number.isFinite(xStart) && Number.isFinite(xEnd) ? [xStart, xEnd] : null;
      }

      if (!nextYRange) {
        const yStart = Number(event["yaxis.range[0]"]);
        const yEnd = Number(event["yaxis.range[1]"]);
        nextYRange =
          Number.isFinite(yStart) && Number.isFinite(yEnd) ? [yStart, yEnd] : null;
      }

      const update: Record<string, AxisRange> = {};

      if (initialXRange && nextXRange) {
        const maxXSpan = rangeSpan(initialXRange) * maxZoomFactor;
        let limited = limitRangeSpan(nextXRange, maxXSpan);
        if (panBounds?.x) {
          limited = clampRange(limited, panBounds.x);
        }
        if (!rangesMatch(nextXRange, limited)) {
          update["xaxis.range"] = limited;
        }
      }

      if (initialYRange && nextYRange) {
        const maxYSpan = rangeSpan(initialYRange) * maxZoomFactor;
        let limited = limitRangeSpan(nextYRange, maxYSpan);
        if (panBounds?.y) {
          limited = clampRange(limited, panBounds.y);
        }
        if (!rangesMatch(nextYRange, limited)) {
          update["yaxis.range"] = limited;
        }
      }

      if (Object.keys(update).length > 0) {
        void Plotly.relayout(graphRef.current as never, update as never);
      }
    },
    [initialXRange, initialYRange, maxZoomFactor, panBounds],
  );

  return (
    <div
      className="min-h-[320px] overflow-hidden rounded-lg border border-slate-200 bg-white"
      onPointerCancel={handlePointerUp}
      onPointerDownCapture={handlePointerDown}
      onPointerMoveCapture={handlePointerMove}
      onPointerUp={handlePointerUp}
    >
      <Plot
        data={data as never}
        layout={{
          autosize: true,
          dragmode: panBounds ? false : "pan",
          height,
          hovermode: "closest",
          paper_bgcolor: "#ffffff",
          plot_bgcolor: "#fbfdff",
          font: { color: "#1f2937", family: "Inter, sans-serif" },
          margin: { l: 56, r: 28, t: 34, b: 54 },
          xaxis: {
            ...axisStyle,
            ...xAxis,
          },
          yaxis: {
            ...axisStyle,
            ...yAxis,
          },
          legend: {
            bgcolor: "rgba(255, 255, 255, 0.92)",
            bordercolor: "#e2e8f0",
            borderwidth: 1,
            orientation: "h",
            x: 0,
            y: 1.14,
            font: { color: "#334155", size: 11 },
          },
          hoverlabel: {
            bgcolor: "#111827",
            bordercolor: "#111827",
            font: { color: "#ffffff", family: "Inter, sans-serif", size: 12 },
          },
          ...restLayout,
        } as never}
        onInitialized={(_, graphDiv) => {
          graphRef.current = graphDiv as PlotlyGraphDiv;
        }}
        onUpdate={(_, graphDiv) => {
          graphRef.current = graphDiv as PlotlyGraphDiv;
        }}
        onPurge={() => {
          if (animationFrameRef.current !== null) {
            window.cancelAnimationFrame(animationFrameRef.current);
          }
          animationFrameRef.current = null;
          graphRef.current = null;
          dragRef.current = null;
        }}
        onRelayout={handleRelayout as never}
        config={{
          displaylogo: false,
          responsive: true,
          modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"],
          toImageButtonOptions: {
            format: "png",
            filename: "grafica-ecc",
            scale: 2,
          },
        }}
        useResizeHandler
        style={{ width: "100%", height }}
      />
    </div>
  );
});

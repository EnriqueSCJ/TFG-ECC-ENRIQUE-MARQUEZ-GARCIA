import { useEffect, useMemo } from "react";
import { cn } from "../../lib/styles";
import { curveRhs, formatNumber, formatPoint } from "../../lib/eccMath";
import { AffinePoint, CurveParameters, FiniteCurvePoint } from "../../types/ecc";
import { SegmentedControl } from "./SegmentedControl";

type Branch = "upper" | "lower";

interface RealPointSelectorProps {
  label: string;
  value: AffinePoint;
  parameters: CurveParameters;
  onChange: (point: AffinePoint) => void;
}

interface FinitePointSelectProps {
  label: string;
  value: AffinePoint;
  points: FiniteCurvePoint[];
  onChange: (point: AffinePoint) => void;
  className?: string;
}

const REAL_X_MIN = -4.5;
const REAL_X_MAX = 4.5;
const REAL_X_SCAN_SAMPLES = 900;

interface RealXBounds {
  min: number;
  max: number;
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function isRealX(x: number, parameters: CurveParameters): boolean {
  return curveRhs(x, parameters.a, parameters.b) >= -1e-8;
}

function refineRealBoundary(
  validX: number,
  invalidX: number,
  parameters: CurveParameters,
): number {
  let valid = validX;
  let invalid = invalidX;

  for (let iteration = 0; iteration < 48; iteration += 1) {
    const mid = (valid + invalid) / 2;
    if (isRealX(mid, parameters)) {
      valid = mid;
    } else {
      invalid = mid;
    }
  }

  return valid;
}

function realCurveXBounds(parameters: CurveParameters): RealXBounds {
  const step = (REAL_X_MAX - REAL_X_MIN) / REAL_X_SCAN_SAMPLES;
  let min: number | null = null;
  let max: number | null = null;
  let previousX = REAL_X_MIN;
  let previousValid = isRealX(previousX, parameters);

  if (previousValid) {
    min = previousX;
    max = previousX;
  }

  for (let index = 1; index <= REAL_X_SCAN_SAMPLES; index += 1) {
    const currentX = REAL_X_MIN + index * step;
    const currentValid = isRealX(currentX, parameters);

    if (currentValid) {
      if (min === null) {
        min = previousValid
          ? currentX
          : refineRealBoundary(currentX, previousX, parameters);
      }
      max = currentX;
    } else if (previousValid) {
      max = refineRealBoundary(previousX, currentX, parameters);
    }

    previousX = currentX;
    previousValid = currentValid;
  }

  return {
    min: Number((min ?? REAL_X_MIN).toFixed(6)),
    max: Number((max ?? REAL_X_MAX).toFixed(6)),
  };
}

function snapToRealX(x: number, parameters: CurveParameters, bounds: RealXBounds): number {
  const requested = clamp(x, bounds.min, bounds.max);
  if (curveRhs(requested, parameters.a, parameters.b) >= 0) return requested;

  const step = 0.02;
  const maxSteps = Math.ceil((bounds.max - bounds.min) / step);

  for (let index = 1; index <= maxSteps; index += 1) {
    const left = clamp(requested - index * step, bounds.min, bounds.max);
    const right = clamp(requested + index * step, bounds.min, bounds.max);

    if (curveRhs(left, parameters.a, parameters.b) >= 0) return left;
    if (curveRhs(right, parameters.a, parameters.b) >= 0) return right;
  }

  return requested;
}

function pointOnRealCurve(
  requestedX: number,
  branch: Branch,
  parameters: CurveParameters,
  label: string,
  bounds: RealXBounds,
): AffinePoint {
  const x = snapToRealX(requestedX, parameters, bounds);
  const rhs = Math.max(curveRhs(x, parameters.a, parameters.b), 0);
  const y = Math.sqrt(rhs) * (branch === "upper" ? 1 : -1);

  return {
    x: Number(x.toFixed(6)),
    y: Number(y.toFixed(6)),
    label,
  };
}

function pointKey(point: AffinePoint): string {
  return point.x === null || point.y === null ? "" : `${point.x},${point.y}`;
}

function hasFinitePoint(points: FiniteCurvePoint[], value: AffinePoint): boolean {
  return points.some((point) => point.x === value.x && point.y === value.y);
}

export function RealPointSelector({
  label,
  value,
  parameters,
  onChange,
}: RealPointSelectorProps) {
  const branch: Branch = (value.y ?? 1) >= 0 ? "upper" : "lower";
  const x = typeof value.x === "number" ? value.x : 0;
  const xBounds = useMemo(
    () => realCurveXBounds(parameters),
    [parameters.a, parameters.b],
  );
  const sliderX = clamp(x, xBounds.min, xBounds.max);

  useEffect(() => {
    const nextPoint = pointOnRealCurve(x, branch, parameters, label, xBounds);
    const currentDistance = Math.abs((value.y ?? 0) - (nextPoint.y ?? 0));

    if (value.x !== nextPoint.x || currentDistance > 0.0005) {
      onChange(nextPoint);
    }
  }, [branch, label, onChange, parameters, value.x, value.y, x, xBounds]);

  return (
    <div className="grid gap-3 rounded-md border border-slate-200 bg-slate-50/80 p-3 text-sm">
      <div className="flex items-center justify-between gap-3">
        <span className="font-medium text-slate-800">{label}</span>
        <span className="rounded border border-slate-200 bg-white px-2 py-1 font-mono text-xs text-slate-700">
          {formatPoint(value)}
        </span>
      </div>

      <label className="grid gap-2 text-slate-700">
        <span className="flex items-center justify-between gap-3">
          <span>x</span>
          <span className="font-mono text-xs text-slate-500">{formatNumber(sliderX, 2)}</span>
        </span>
        <input
          type="range"
          value={sliderX}
          min={xBounds.min}
          max={xBounds.max}
          step={0.05}
          onChange={(event) =>
            onChange(
              pointOnRealCurve(Number(event.target.value), branch, parameters, label, xBounds),
            )
          }
          className="h-2 cursor-pointer accent-indigo-700"
        />
      </label>

      <SegmentedControl
        value={branch}
        onChange={(nextBranch) =>
          onChange(pointOnRealCurve(sliderX, nextBranch, parameters, label, xBounds))
        }
        options={[
          { value: "upper", label: "Rama superior" },
          { value: "lower", label: "Rama inferior" },
        ]}
      />
    </div>
  );
}

export function FinitePointSelect({
  label,
  value,
  points,
  onChange,
  className,
}: FinitePointSelectProps) {
  useEffect(() => {
    if (points.length > 0 && !hasFinitePoint(points, value)) {
      const [firstPoint] = points;
      onChange({ x: firstPoint.x, y: firstPoint.y, label });
    }
  }, [label, onChange, points, value]);

  return (
    <label className={cn("grid gap-2 text-sm text-slate-700", className)}>
      <span className="font-medium text-slate-800">{label}</span>
      <select
        value={pointKey(value)}
        onChange={(event) => {
          const [x, y] = event.target.value.split(",").map(Number);
          if (Number.isFinite(x) && Number.isFinite(y)) {
            onChange({ x, y, label });
          }
        }}
        className="h-10 rounded-md border border-slate-300 bg-white px-3 font-mono text-sm text-slate-900 outline-none transition focus:border-indigo-700 focus:ring-2 focus:ring-indigo-100"
      >
        <option value="" disabled>
          Sin punto seleccionado
        </option>
        {points.map((point) => (
          <option key={`${point.x},${point.y}`} value={`${point.x},${point.y}`}>
            ({point.x}, {point.y})
          </option>
        ))}
      </select>
    </label>
  );
}

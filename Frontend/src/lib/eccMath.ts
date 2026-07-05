import {
  AffinePoint,
  CurveParameters,
  GroupOperationResult,
  POINT_INFINITY,
  isPointAtInfinity,
} from "../types/ecc";

const EPSILON = 1e-8;

export function curveRhs(x: number, a: number, b: number): number {
  return x ** 3 + a * x + b;
}

export function realDiscriminant(a: number, b: number): number {
  return -16 * (4 * a ** 3 + 27 * b ** 2);
}

function bisectCurveRoot(left: number, right: number, a: number, b: number): number {
  let low = left;
  let high = right;
  let lowValue = curveRhs(low, a, b);

  for (let iteration = 0; iteration < 64; iteration += 1) {
    const mid = (low + high) / 2;
    const midValue = curveRhs(mid, a, b);

    if (Math.abs(midValue) < EPSILON) return mid;

    if (lowValue * midValue <= 0) {
      high = mid;
    } else {
      low = mid;
      lowValue = midValue;
    }
  }

  return (low + high) / 2;
}

function addSample(sampleXs: number[], value: number): void {
  if (!sampleXs.some((sample) => Math.abs(sample - value) < 1e-5)) {
    sampleXs.push(value);
  }
}

export function buildContinuousCurve(
  a: number,
  b: number,
  xMin = -4,
  xMax = 4,
  samples = 360,
): { x: number[]; upper: Array<number | null>; lower: Array<number | null> } {
  const x: number[] = [];
  const upper: Array<number | null> = [];
  const lower: Array<number | null> = [];
  const step = (xMax - xMin) / samples;
  const sampleXs: number[] = [];

  for (let index = 0; index <= samples; index += 1) {
    addSample(sampleXs, xMin + index * step);
  }

  const scanXs = [...sampleXs];

  for (let index = 1; index < scanXs.length; index += 1) {
    const previousX = scanXs[index - 1];
    const currentX = scanXs[index];
    const previousValue = curveRhs(previousX, a, b);
    const currentValue = curveRhs(currentX, a, b);

    if (Math.abs(previousValue) < EPSILON) addSample(sampleXs, previousX);
    if (Math.abs(currentValue) < EPSILON) addSample(sampleXs, currentX);

    if (previousValue * currentValue < 0) {
      addSample(sampleXs, bisectCurveRoot(previousX, currentX, a, b));
    }
  }

  sampleXs.sort((left, right) => left - right);

  for (const currentX of sampleXs) {
    const rhs = curveRhs(currentX, a, b);
    x.push(Number(currentX.toFixed(4)));

    if (rhs >= -EPSILON) {
      const y = Math.sqrt(Math.max(rhs, 0));
      upper.push(y);
      lower.push(-y);
    } else {
      upper.push(null);
      lower.push(null);
    }
  }

  return { x, upper, lower };
}

export function isOnRealCurve(point: AffinePoint, parameters: CurveParameters): boolean {
  if (isPointAtInfinity(point) || point.x === null || point.y === null) return false;
  return Math.abs(point.y ** 2 - curveRhs(point.x, parameters.a, parameters.b)) < 0.08;
}

export function realGroupOperation(
  left: AffinePoint,
  right: AffinePoint,
  parameters: CurveParameters,
  mode: "add" | "double",
  lineXRange: [number, number] = [-4.5, 4.5],
): GroupOperationResult {
  const rightPoint = mode === "double" ? left : right;

  if (
    left.x === null ||
    left.y === null ||
    rightPoint.x === null ||
    rightPoint.y === null
  ) {
    throw new Error("La visualización real requiere puntos afines finitos.");
  }

  if (!isOnRealCurve(left, parameters) || !isOnRealCurve(rightPoint, parameters)) {
    throw new Error("Los puntos deben estar sobre la curva real para trazar cuerda o tangente.");
  }

  const leftX = left.x;
  const leftY = left.y;
  const rightX = rightPoint.x;
  const rightY = rightPoint.y;
  const isDoubling = mode === "double" || (leftX === rightX && leftY === rightY);
  const denominator = isDoubling ? 2 * leftY : rightX - leftX;

  if (Math.abs(denominator) < EPSILON) {
    return {
      result: { ...POINT_INFINITY },
      steps: [
        {
          title: "Recta vertical",
          description: "La recta corta a la curva en el punto del infinito.",
          latex: "P+(-P)=\\mathcal{O}",
        },
      ],
    };
  }

  const slope = isDoubling
    ? (3 * leftX ** 2 + parameters.a) / denominator
    : (rightY - leftY) / denominator;
  const xIntersection = slope ** 2 - leftX - rightX;
  const yIntersection = slope * (xIntersection - leftX) + leftY;
  const result = {
    x: xIntersection,
    y: -yIntersection,
  };
  const lineX = [...lineXRange];
  const lineY = lineX.map((x) => slope * (x - leftX) + leftY);

  return {
    result,
    reflectedPoint: { x: xIntersection, y: yIntersection },
    slope,
    line: { x: lineX, y: lineY },
    steps: [
      {
        title: isDoubling ? "Tangente" : "Cuerda",
        description: isDoubling
          ? "La pendiente se calcula con la derivada implicita."
          : "La pendiente se calcula con los dos puntos seleccionados.",
        latex: isDoubling
          ? "\\lambda=\\frac{3x_1^2+a}{2y_1}"
          : "\\lambda=\\frac{y_2-y_1}{x_2-x_1}",
      },
      {
        title: "Tercer corte",
        description: `El tercer corte tiene x = ${formatNumber(xIntersection)}.`,
        latex: "x_3=\\lambda^2-x_1-x_2",
      },
      {
        title: "Reflexion",
        description: "El resultado P+Q es la reflexión del tercer corte sobre el eje x.",
        latex: "P+Q=(x_3,-y_3)",
      },
    ],
  };
}

export function formatNumber(value: number | null | undefined, digits = 3): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "𝒪";
  if (Number.isInteger(value)) return value.toString();
  return value.toFixed(digits).replace(/\.?0+$/, "");
}

export function formatPoint(point: AffinePoint): string {
  if (isPointAtInfinity(point)) return "𝒪";
  return `(${formatNumber(point.x)}, ${formatNumber(point.y)})`;
}

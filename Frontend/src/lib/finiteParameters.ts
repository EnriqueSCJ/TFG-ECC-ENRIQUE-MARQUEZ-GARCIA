import type { CurveParameters } from "../types/ecc";

type CurveCoefficientDraft = Pick<CurveParameters, "a" | "b">;

export function hasIntegerCurveCoefficients(parameters: CurveCoefficientDraft): boolean {
  return Number.isInteger(parameters.a) && Number.isInteger(parameters.b);
}

export function roundCurveCoefficients(parameters: CurveCoefficientDraft): CurveCoefficientDraft {
  return {
    a: Math.round(parameters.a),
    b: Math.round(parameters.b),
  };
}

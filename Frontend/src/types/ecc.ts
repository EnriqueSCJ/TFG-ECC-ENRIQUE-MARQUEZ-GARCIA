export type ModuleId =
  | "learning-path"
  | "weierstrass"
  | "group-law"
  | "finite-fields"
  | "ecdlp"
  | "protocols"
  | "audit-attacks";

export interface CurveParameters {
  a: number;
  b: number;
  p: number;
  gx: number;
  gy: number;
  n?: number;
  h?: number;
  name?: string;
}

export interface AffinePoint {
  x: number | null;
  y: number | null;
  label?: string;
}

export interface FiniteCurvePoint {
  x: number;
  y: number;
  label?: string;
}

export interface OperationStep {
  title: string;
  description: string;
  latex?: string;
}

export interface GroupOperationResult {
  result: AffinePoint;
  slope?: number;
  line?: {
    x: number[];
    y: number[];
  };
  reflectedPoint?: AffinePoint;
  steps: OperationStep[];
}

export interface ScalarWalkStep {
  index: number;
  point: AffinePoint;
  action: string;
}

export interface PollardsRhoStep {
  index: number;
  point: AffinePoint;
  alpha: number;
  beta: number;
  action: string;
  partition: number;
}

export interface PollardsRhoCollision {
  firstIndex: number;
  secondIndex: number;
  point: AffinePoint;
  alphaDelta?: number;
  betaDelta?: number;
  recoveredSecret?: number | null;
  candidateSecrets?: number[];
  note?: string;
}

export interface ApiErrorPayload {
  detail?: string;
  error?: string;
  message?: string;
}

export interface CurveValidationResponse {
  valid: boolean;
  message: string;
  discriminant: number | null;
}

export interface FinitePointsResponse {
  points: FiniteCurvePoint[];
  discriminant: number;
}

export interface ScalarMultiplicationResponse {
  result: AffinePoint;
  steps: OperationStep[];
  walk: ScalarWalkStep[];
}

export interface PollardsRhoResponse {
  target: AffinePoint;
  order: number;
  steps: PollardsRhoStep[];
  collision: PollardsRhoCollision | null;
}

export interface FactorizationTerm {
  factor: number;
  exponent: number;
}

export interface BabyStepGiantStepResponse {
  order: number;
  target: AffinePoint;
  m: number;
  babySteps: Array<{ index: number; point: AffinePoint }>;
  giantSteps: Array<{ index: number; point: AffinePoint; matchedBabyIndex?: number }>;
  result: number | null;
  found: boolean;
}

export interface AuditResponse {
  totalPoints: number;
  order: number;
  factors: FactorizationTerm[];
  cofactor: number | null;
  largestPrimeFactor: number | null;
  isAnomalous: boolean;
}

export interface EcdhResponse {
  order: number;
  alicePrivate: number;
  bobPrivate: number;
  alicePublic: AffinePoint;
  bobPublic: AffinePoint;
  sharedByAlice: AffinePoint;
  sharedByBob: AffinePoint;
  matches: boolean;
}

export interface EcdsaResponse {
  order: number;
  privateKey: number;
  publicKey: AffinePoint;
  nonce: number;
  hash: number;
  signature: { r: number; s: number };
  verification: { u1: number; u2: number; point: AffinePoint; valid: boolean };
}

export const POINT_INFINITY: AffinePoint = Object.freeze({
  x: null,
  y: null,
  label: "𝒪",
});

export const isPointAtInfinity = (point: AffinePoint): boolean =>
  point.x === null && point.y === null;

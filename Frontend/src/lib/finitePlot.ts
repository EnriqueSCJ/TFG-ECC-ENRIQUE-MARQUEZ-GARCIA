export function finiteAxisStep(p: number): number {
  if (p <= 31) return 1;
  if (p <= 101) return 10;
  if (p <= 251) return 25;
  if (p <= 503) return 50;
  return Math.max(100, Math.ceil(p / 10));
}

export function finiteMarkerSize(p: number): number {
  if (p <= 101) return 9;
  if (p <= 251) return 7;
  if (p <= 503) return 6;
  return 5;
}

export function finiteBackgroundMarkerSize(p: number): number {
  if (p <= 101) return 8;
  if (p <= 251) return 6;
  if (p <= 503) return 5;
  return 4;
}

export function shouldUseDetailedFiniteHover(p: number): boolean {
  return p <= 251;
}

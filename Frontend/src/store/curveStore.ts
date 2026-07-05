import { create } from "zustand";
import { AffinePoint, CurveParameters, ModuleId } from "../types/ecc";

interface CurveStore {
  activeModule: ModuleId;
  parameters: CurveParameters;
  pointP: AffinePoint;
  pointQ: AffinePoint;
  scalarK: number;
  apiError: string | null;
  setActiveModule: (moduleId: ModuleId) => void;
  setParameters: (parameters: Partial<CurveParameters>) => void;
  setPointP: (point: Partial<AffinePoint>) => void;
  setPointQ: (point: Partial<AffinePoint>) => void;
  setScalarK: (scalar: number) => void;
  setApiError: (message: string | null) => void;
}

export const useCurveStore = create<CurveStore>((set) => ({
  activeModule: "weierstrass",
  parameters: {
    a: -1,
    b: 1,
    p: 17,
    gx: 0,
    gy: 1,
    n: 14,
    h: 1,
    name: "E: y^2 = x^3 - x + 1",
  },
  pointP: { x: 0, y: 1, label: "P" },
  pointQ: { x: 1, y: 1, label: "Q" },
  scalarK: 9,
  apiError: null,
  setActiveModule: (moduleId) => set({ activeModule: moduleId }),
  setParameters: (parameters) =>
    set((state) => ({
      parameters: {
        ...state.parameters,
        ...parameters,
      },
    })),
  setPointP: (point) =>
    set((state) => ({
      pointP: {
        ...state.pointP,
        ...point,
      },
    })),
  setPointQ: (point) =>
    set((state) => ({
      pointQ: {
        ...state.pointQ,
        ...point,
      },
    })),
  setScalarK: (scalarK) => set({ scalarK }),
  setApiError: (apiError) => set({ apiError }),
}));

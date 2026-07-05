import { apiClient } from "./apiClient";
import {
  AffinePoint,
  AuditResponse,
  BabyStepGiantStepResponse,
  CurveParameters,
  CurveValidationResponse,
  EcdhResponse,
  EcdsaResponse,
  FinitePointsResponse,
  GroupOperationResult,
  PollardsRhoResponse,
  ScalarMultiplicationResponse,
} from "../types/ecc";

export const eccService = {
  async validateCurve(parameters: CurveParameters): Promise<CurveValidationResponse> {
    const { data } = await apiClient.post<CurveValidationResponse>("/ecc/curve/validate", parameters);
    return data;
  },

  async getFinitePoints(parameters: CurveParameters): Promise<FinitePointsResponse> {
    const { data } = await apiClient.post<FinitePointsResponse>("/ecc/finite-points", parameters);
    return data;
  },

  async addPoints(
    parameters: CurveParameters,
    left: AffinePoint,
    right: AffinePoint,
  ): Promise<GroupOperationResult> {
    const { data } = await apiClient.post<GroupOperationResult>("/ecc/group/add", {
      parameters,
      left,
      right,
    });
    return data;
  },

  async multiplyPoint(
    parameters: CurveParameters,
    point: AffinePoint,
    scalar: number,
  ): Promise<ScalarMultiplicationResponse> {
    const { data } = await apiClient.post<ScalarMultiplicationResponse>(
      "/ecc/scalar-multiply",
      {
        parameters,
        point,
        scalar,
      },
    );
    return data;
  },

  async pollardsRho(
    parameters: CurveParameters,
    generator: AffinePoint,
    secretScalar: number,
    maxSteps: number,
  ): Promise<PollardsRhoResponse> {
    const { data } = await apiClient.post<PollardsRhoResponse>("/attacks/pollards-rho", {
      parameters,
      generator,
      secretScalar,
      maxSteps,
    });
    return data;
  },

  async babyStepGiantStep(
    parameters: CurveParameters,
    generator: AffinePoint,
    secretScalar: number,
  ): Promise<BabyStepGiantStepResponse> {
    const { data } = await apiClient.post<BabyStepGiantStepResponse>(
      "/attacks/baby-step-giant-step",
      { parameters, generator, secretScalar },
    );
    return data;
  },

  async audit(parameters: CurveParameters, generator: AffinePoint): Promise<AuditResponse> {
    const { data } = await apiClient.post<AuditResponse>("/attacks/audit", {
      parameters,
      generator,
    });
    return data;
  },

  async simulateEcdh(
    parameters: CurveParameters,
    generator: AffinePoint,
    aliceSecret: number,
    bobSecret: number,
  ): Promise<EcdhResponse> {
    const { data } = await apiClient.post<EcdhResponse>("/protocols/ecdh", {
      parameters,
      generator,
      aliceSecret,
      bobSecret,
    });
    return data;
  },

  async simulateEcdsa(
    parameters: CurveParameters,
    generator: AffinePoint,
    privateSecret: number,
    nonce: number,
    message: string,
  ): Promise<EcdsaResponse> {
    const { data } = await apiClient.post<EcdsaResponse>("/protocols/ecdsa", {
      parameters,
      generator,
      privateSecret,
      nonce,
      message,
    });
    return data;
  },
};

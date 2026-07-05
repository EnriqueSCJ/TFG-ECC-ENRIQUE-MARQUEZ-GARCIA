from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CurveParametersIn(StrictBaseModel):
    a: StrictInt
    b: StrictInt
    p: StrictInt
    gx: StrictInt = 0
    gy: StrictInt = 0
    n: StrictInt | None = None
    h: StrictInt | None = 1
    name: StrictStr | None = None


class AffinePointIn(StrictBaseModel):
    x: StrictInt | None
    y: StrictInt | None
    label: StrictStr | None = None


class AddPointsRequest(StrictBaseModel):
    parameters: CurveParametersIn
    left: AffinePointIn
    right: AffinePointIn


class ScalarMultiplyRequest(StrictBaseModel):
    parameters: CurveParametersIn
    point: AffinePointIn
    scalar: StrictInt


class PollardsRhoRequest(StrictBaseModel):
    parameters: CurveParametersIn
    generator: AffinePointIn
    secretScalar: StrictInt
    maxSteps: StrictInt = Field(default=48, ge=1, le=160)


class BabyStepGiantStepRequest(StrictBaseModel):
    parameters: CurveParametersIn
    generator: AffinePointIn
    secretScalar: StrictInt


class AuditRequest(StrictBaseModel):
    parameters: CurveParametersIn
    generator: AffinePointIn


class EcdhRequest(StrictBaseModel):
    parameters: CurveParametersIn
    generator: AffinePointIn
    aliceSecret: StrictInt
    bobSecret: StrictInt


class EcdsaRequest(StrictBaseModel):
    parameters: CurveParametersIn
    generator: AffinePointIn
    privateSecret: StrictInt
    nonce: StrictInt
    message: StrictStr

from __future__ import annotations

from fastapi import APIRouter

from ..api_utils import build_curve, build_point, domain_error
from ..schemas import AuditRequest, BabyStepGiantStepRequest, PollardsRhoRequest
from ..services.attacks import simulate_baby_step_giant_step, simulate_pollards_rho
from ..services.elliptic_curve import audit_curve
from ..services.errors import EccDomainError

router = APIRouter(prefix="/attacks", tags=["attacks"])


@router.post("/pollards-rho")
def pollards_rho(request: PollardsRhoRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        generator = build_point(curve, request.generator)
        return simulate_pollards_rho(generator, request.secretScalar, request.maxSteps)
    except EccDomainError as error:
        raise domain_error(error)


@router.post("/baby-step-giant-step")
def baby_step_giant_step(request: BabyStepGiantStepRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        generator = build_point(curve, request.generator)
        return simulate_baby_step_giant_step(generator, request.secretScalar)
    except EccDomainError as error:
        raise domain_error(error)


@router.post("/audit")
def audit(request: AuditRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        generator = build_point(curve, request.generator)
        return audit_curve(curve, generator)
    except EccDomainError as error:
        raise domain_error(error)


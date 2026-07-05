from __future__ import annotations

from fastapi import APIRouter

from ..api_utils import build_curve, build_point, domain_error
from ..schemas import EcdhRequest, EcdsaRequest
from ..services.errors import EccDomainError
from ..services.protocols import simulate_ecdh, simulate_ecdsa

router = APIRouter(prefix="/protocols", tags=["protocols"])


@router.post("/ecdh")
def ecdh(request: EcdhRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        generator = build_point(curve, request.generator)
        return simulate_ecdh(generator, request.aliceSecret, request.bobSecret)
    except EccDomainError as error:
        raise domain_error(error)


@router.post("/ecdsa")
def ecdsa(request: EcdsaRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        generator = build_point(curve, request.generator)
        return simulate_ecdsa(generator, request.privateSecret, request.nonce, request.message)
    except EccDomainError as error:
        raise domain_error(error)


from __future__ import annotations

from fastapi import APIRouter

from ..api_utils import build_curve, build_point, domain_error
from ..schemas import AddPointsRequest, CurveParametersIn, ScalarMultiplyRequest
from ..services.elliptic_curve import add_points, finite_curve_points, multiply_point, scalar_multiplication_walk
from ..services.errors import EccDomainError

router = APIRouter(prefix="/ecc", tags=["ecc"])


@router.post("/curve/validate")
def validate_curve(parameters: CurveParametersIn) -> dict[str, object]:
    try:
        curve = build_curve(parameters)
        return {
            "valid": True,
            "message": "La curva define un grupo elíptico no singular sobre F_p.",
            "discriminant": curve.discriminant,
        }
    except EccDomainError as error:
        return {"valid": False, "message": str(error), "discriminant": None}


@router.post("/finite-points")
def get_finite_points(parameters: CurveParametersIn) -> dict[str, object]:
    try:
        curve = build_curve(parameters)
        return {
            "points": finite_curve_points(curve),
            "discriminant": curve.discriminant,
        }
    except EccDomainError as error:
        raise domain_error(error)


@router.post("/group/add")
def add_group_points(request: AddPointsRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        left = build_point(curve, request.left)
        right = build_point(curve, request.right)
        return add_points(left, right)
    except EccDomainError as error:
        raise domain_error(error)


@router.post("/scalar-multiply")
def scalar_multiply(request: ScalarMultiplyRequest) -> dict[str, object]:
    try:
        curve = build_curve(request.parameters)
        point = build_point(curve, request.point)
        product = multiply_point(request.scalar, point)
        return {
            "result": product["result"],
            "steps": product["steps"],
            "walk": scalar_multiplication_walk(request.scalar, point),
        }
    except EccDomainError as error:
        raise domain_error(error)

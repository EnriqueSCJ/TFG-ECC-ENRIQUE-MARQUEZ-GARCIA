from __future__ import annotations

from fastapi import HTTPException

from .schemas import AffinePointIn, CurveParametersIn
from .services.elliptic_curve import Curve, Point
from .services.errors import EccDomainError


def build_curve(parameters: CurveParametersIn) -> Curve:
    return Curve(
        a=parameters.a,
        b=parameters.b,
        p=parameters.p,
        gx=parameters.gx,
        gy=parameters.gy,
        n=parameters.n,
        h=parameters.h if parameters.h is not None else 1,
        name=parameters.name,
    )


def build_point(curve: Curve, point: AffinePointIn) -> Point:
    return curve.point(point.x, point.y, point.label)


def domain_error(error: EccDomainError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(error))

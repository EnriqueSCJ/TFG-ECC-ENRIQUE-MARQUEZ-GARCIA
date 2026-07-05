from __future__ import annotations

from dataclasses import dataclass

from .errors import EccDomainError
from .number_theory import factor_integer, gcd, is_prime, mod, mod_inverse


MAX_PRIME = 997
POINT_INFINITY = {"x": None, "y": None, "label": "𝒪"}


@dataclass(frozen=True)
class Curve:
    a: int
    b: int
    p: int
    gx: int | None = None
    gy: int | None = None
    n: int | None = None
    h: int = 1
    name: str | None = None

    def __post_init__(self) -> None:
        if self.p <= 3:
            raise EccDomainError("La caracteristica debe ser un primo p > 3.")
        if self.p > MAX_PRIME:
            raise EccDomainError(
                f"El backend didáctico limita p a {MAX_PRIME} para mantener cálculos interactivos."
            )
        if not is_prime(self.p):
            raise EccDomainError("El parametro p debe ser primo.")
        object.__setattr__(self, "a", self.a % self.p)
        object.__setattr__(self, "b", self.b % self.p)
        if self.discriminant == 0:
            raise EccDomainError("La curva es singular: Delta equivale a 0 módulo p.")
        if self.n is not None and self.n <= 0:
            raise EccDomainError("El orden n debe ser positivo.")
        if self.h <= 0:
            raise EccDomainError("El cofactor h debe ser positivo.")

    @property
    def discriminant(self) -> int:
        return mod(-16 * (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)), self.p)

    def contains_coordinates(self, x: int, y: int) -> bool:
        return mod(y * y, self.p) == mod(pow(x, 3, self.p) + self.a * x + self.b, self.p)

    def point(self, x: int | None, y: int | None, label: str | None = None) -> "Point":
        return Point(self, x, y, label)


@dataclass(frozen=True)
class Point:
    curve: Curve
    x: int | None
    y: int | None
    label: str | None = None

    def __post_init__(self) -> None:
        if (self.x is None) != (self.y is None):
            raise EccDomainError("El punto del infinito debe tener x = null e y = null.")
        if self.is_infinity:
            return

        x = int(self.x) % self.curve.p
        y = int(self.y) % self.curve.p
        if not self.curve.contains_coordinates(x, y):
            raise EccDomainError(f"El punto ({self.x}, {self.y}) no pertenece a la curva.")
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    @property
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    def negate(self) -> "Point":
        if self.is_infinity:
            return self
        return Point(self.curve, self.x, -self.y)

    def to_payload(self) -> dict[str, int | str | None]:
        if self.is_infinity:
            return dict(POINT_INFINITY)
        payload: dict[str, int | str | None] = {"x": self.x, "y": self.y}
        if self.label:
            payload["label"] = self.label
        return payload


@dataclass(frozen=True)
class _JacobianPoint:
    curve: Curve
    x: int
    y: int
    z: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", self.x % self.curve.p)
        object.__setattr__(self, "y", self.y % self.curve.p)
        object.__setattr__(self, "z", self.z % self.curve.p)

    @property
    def is_infinity(self) -> bool:
        return self.z == 0


def format_point(point: Point) -> str:
    if point.is_infinity:
        return "O"
    return f"({point.x}, {point.y})"


def _jacobian_infinity(curve: Curve) -> _JacobianPoint:
    return _JacobianPoint(curve, 0, 1, 0)


def _affine_to_jacobian(point: Point) -> _JacobianPoint:
    if point.is_infinity:
        return _jacobian_infinity(point.curve)
    return _JacobianPoint(point.curve, point.x or 0, point.y or 0, 1)


def _jacobian_to_affine(point: _JacobianPoint) -> Point:
    if point.is_infinity:
        return point.curve.point(None, None)

    p = point.curve.p
    z_inverse = mod_inverse(point.z, p)
    z_inverse_squared = (z_inverse * z_inverse) % p
    x = (point.x * z_inverse_squared) % p
    y = (point.y * z_inverse_squared * z_inverse) % p
    return point.curve.point(x, y)


def _ensure_same_jacobian_curve(left: _JacobianPoint, right: _JacobianPoint) -> None:
    if left.curve != right.curve:
        raise EccDomainError("Los puntos deben pertenecer a la misma curva.")


def _jacobian_double(point: _JacobianPoint) -> _JacobianPoint:
    if point.is_infinity or point.y == 0:
        return _jacobian_infinity(point.curve)

    curve = point.curve
    p = curve.p
    x, y, z = point.x, point.y, point.z

    yy = (y * y) % p
    yyyy = (yy * yy) % p
    xx = (x * x) % p
    s = (4 * x * yy) % p
    z2 = (z * z) % p
    z4 = (z2 * z2) % p
    m = (3 * xx + curve.a * z4) % p
    x3 = (m * m - 2 * s) % p
    y3 = (m * (s - x3) - 8 * yyyy) % p
    z3 = (2 * y * z) % p

    return _JacobianPoint(curve, x3, y3, z3)


def _jacobian_add(left: _JacobianPoint, right: _JacobianPoint) -> _JacobianPoint:
    _ensure_same_jacobian_curve(left, right)

    if left.is_infinity:
        return right
    if right.is_infinity:
        return left

    curve = left.curve
    p = curve.p
    x1, y1, z1 = left.x, left.y, left.z
    x2, y2, z2 = right.x, right.y, right.z

    z1z1 = (z1 * z1) % p
    z2z2 = (z2 * z2) % p
    u1 = (x1 * z2z2) % p
    u2 = (x2 * z1z1) % p
    s1 = (y1 * z2 * z2z2) % p
    s2 = (y2 * z1 * z1z1) % p
    h = (u2 - u1) % p
    r = (s2 - s1) % p

    if h == 0:
        return _jacobian_double(left) if r == 0 else _jacobian_infinity(curve)

    hh = (h * h) % p
    hhh = (h * hh) % p
    v = (u1 * hh) % p
    x3 = (r * r - hhh - 2 * v) % p
    y3 = (r * (v - x3) - s1 * hhh) % p
    z3 = (h * z1 * z2) % p

    return _JacobianPoint(curve, x3, y3, z3)


def finite_curve_points(curve: Curve) -> list[dict[str, int | str]]:
    residues: dict[int, list[int]] = {}
    for y in range(curve.p):
        residues.setdefault((y * y) % curve.p, []).append(y)

    points: list[dict[str, int | str]] = []
    for x in range(curve.p):
        rhs = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p
        for y in residues.get(rhs, []):
            points.append({"x": x, "y": y, "label": f"({x}, {y})"})
    return points


def curve_group_order(curve: Curve) -> int:
    return len(finite_curve_points(curve)) + 1


def add_points_fast(left: Point, right: Point) -> Point:
    return _jacobian_to_affine(_jacobian_add(_affine_to_jacobian(left), _affine_to_jacobian(right)))


def add_points(left: Point, right: Point) -> dict[str, object]:
    if left.curve != right.curve:
        raise EccDomainError("Los puntos deben pertenecer a la misma curva.")

    steps: list[dict[str, str]] = []
    curve = left.curve
    p = curve.p

    if left.is_infinity:
        steps.append(
            {"title": "Elemento neutro", "description": "𝒪 + Q devuelve Q.", "latex": r"\mathcal{O}+Q=Q"}
        )
        return {"result": right.to_payload(), "steps": steps}
    if right.is_infinity:
        steps.append(
            {"title": "Elemento neutro", "description": "P + 𝒪 devuelve P.", "latex": r"P+\mathcal{O}=P"}
        )
        return {"result": left.to_payload(), "steps": steps}

    x1, y1 = left.x or 0, left.y or 0
    x2, y2 = right.x or 0, right.y or 0

    if x1 == x2 and (y1 + y2) % p == 0:
        steps.append(
            {
                "title": "Recta vertical",
                "description": "P y -P tienen la misma x y ordenadas opuestas.",
                "latex": r"P+(-P)=\mathcal{O}",
            }
        )
        return {"result": dict(POINT_INFINITY), "steps": steps}

    is_doubling = x1 == x2 and y1 == y2
    numerator = (3 * x1 * x1 + curve.a) % p if is_doubling else (y2 - y1) % p
    denominator = (2 * y1) % p if is_doubling else (x2 - x1) % p
    inverse = mod_inverse(denominator, p)
    slope = (numerator * inverse) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    result = Point(curve, x3, y3)

    steps.append(
        {
            "title": "Pendiente de la tangente" if is_doubling else "Pendiente de la secante",
            "description": (
                f"lambda = {slope} con numerador {numerator}, "
                f"denominador {denominator} e inverso {inverse}."
            ),
            "latex": (
                rf"\lambda=\frac{{3x_1^2+a}}{{2y_1}}\equiv {slope}\pmod{{{p}}}"
                if is_doubling
                else rf"\lambda=\frac{{y_2-y_1}}{{x_2-x_1}}\equiv {slope}\pmod{{{p}}}"
            ),
        }
    )
    steps.append(
        {"title": "Coordenada x3", "description": f"x3 = {x3}.", "latex": rf"x_3\equiv {x3}\pmod{{{p}}}"}
    )
    steps.append(
        {"title": "Coordenada y3", "description": f"y3 = {y3}.", "latex": rf"y_3\equiv {y3}\pmod{{{p}}}"}
    )

    return {"result": result.to_payload(), "slope": slope, "steps": steps}


def multiply_point_fast(scalar: int, point: Point) -> Point:
    value = abs(int(scalar))
    if value == 0 or point.is_infinity:
        return point.curve.point(None, None)

    addend = _affine_to_jacobian(point.negate() if scalar < 0 else point)
    result = _jacobian_infinity(point.curve)

    while value > 0:
        if value & 1:
            result = _jacobian_add(result, addend)
        value >>= 1
        if value:
            addend = _jacobian_double(addend)

    return _jacobian_to_affine(result)


def multiply_point(scalar: int, point: Point) -> dict[str, object]:
    steps: list[dict[str, str]] = []
    visited: list[dict[str, object]] = []
    value = abs(int(scalar))
    addend = _affine_to_jacobian(point.negate() if scalar < 0 else point)
    result = _jacobian_infinity(point.curve)
    bit_index = 0

    steps.append(
        {
            "title": "Descomposicion binaria",
            "description": f"Se evalua k = {scalar} con double-and-add en coordenadas Jacobianas.",
            "latex": rf"{value}=({value:b})_2",
        }
    )

    if value == 0 or point.is_infinity:
        return {
            "result": dict(POINT_INFINITY),
            "steps": steps,
            "visited": [{"index": 0, "point": dict(POINT_INFINITY), "action": "inicio"}],
        }

    while value > 0:
        bit = value & 1
        steps.append({"title": f"Bit {bit_index}", "description": f"El bit actual vale {bit}.", "latex": rf"b_{bit_index}={bit}"})

        if bit:
            result = _jacobian_add(result, addend)
            result_affine = _jacobian_to_affine(result)
            visited.append(
                {
                    "index": len(visited) + 1,
                    "point": result_affine.to_payload(),
                    "action": f"acumular bit {bit_index}",
                }
            )
            steps.append(
                {
                    "title": "Acumulacion",
                    "description": f"Resultado parcial: {format_point(result_affine)}.",
                    "latex": r"R\leftarrow R+A",
                }
            )

        value >>= 1
        if value:
            addend = _jacobian_double(addend)
            addend_affine = _jacobian_to_affine(addend)
            visited.append(
                {
                    "index": len(visited) + 1,
                    "point": addend_affine.to_payload(),
                    "action": "doblar acumulado",
                }
            )
            steps.append(
                {
                    "title": "Doblado",
                    "description": f"Nuevo acumulado: {format_point(addend_affine)}.",
                    "latex": r"A\leftarrow 2A",
                }
            )
        bit_index += 1

    return {"result": _jacobian_to_affine(result).to_payload(), "steps": steps, "visited": visited}


def scalar_multiplication_walk(scalar: int, point: Point) -> list[dict[str, object]]:
    limit = min(abs(int(scalar)), 80)
    base = point.negate() if scalar < 0 else point
    current = point.curve.point(None, None)
    walk: list[dict[str, object]] = [{"index": 0, "point": current.to_payload(), "action": "𝒪"}]

    for index in range(1, limit + 1):
        current = add_points_fast(current, base)
        walk.append({"index": index, "point": current.to_payload(), "action": f"{index}P"})

    return walk


def point_order(point: Point, group_order: int | None = None) -> int:
    if point.is_infinity:
        return 1

    order = group_order if group_order is not None else curve_group_order(point.curve)
    if not multiply_point_fast(order, point).is_infinity:
        raise EccDomainError("El orden del grupo no anula el punto; el dominio no es coherente.")

    candidate = order
    for factor in factor_integer(order):
        prime = factor["factor"]
        for _ in range(factor["exponent"]):
            reduced_candidate = candidate // prime
            if multiply_point_fast(reduced_candidate, point).is_infinity:
                candidate = reduced_candidate
            else:
                break

    return candidate


def audit_curve(curve: Curve, generator: Point) -> dict[str, object]:
    total_points = curve_group_order(curve)
    order = point_order(generator, total_points)
    factors = factor_integer(order)
    cofactor = total_points // order if total_points % order == 0 else None
    largest_prime_factor = factors[-1]["factor"] if factors else None

    return {
        "totalPoints": total_points,
        "order": order,
        "factors": factors,
        "cofactor": cofactor,
        "largestPrimeFactor": largest_prime_factor,
        "isAnomalous": total_points == curve.p,
    }


def normalize_private_scalar(value: int, order: int) -> int:
    if order < 2:
        raise EccDomainError("El orden del generador debe ser mayor que 1.")
    return ((int(value) - 1) % (order - 1)) + 1


__all__ = [
    "Curve",
    "MAX_PRIME",
    "POINT_INFINITY",
    "Point",
    "add_points",
    "add_points_fast",
    "audit_curve",
    "curve_group_order",
    "factor_integer",
    "finite_curve_points",
    "format_point",
    "gcd",
    "multiply_point",
    "multiply_point_fast",
    "normalize_private_scalar",
    "point_order",
    "scalar_multiplication_walk",
]

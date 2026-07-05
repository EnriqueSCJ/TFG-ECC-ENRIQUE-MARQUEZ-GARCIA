from __future__ import annotations

import math

from .elliptic_curve import Point, add_points_fast, format_point, multiply_point_fast, point_order
from .errors import EccDomainError
from .number_theory import gcd, mod_inverse


def point_key(point: Point) -> str:
    return "O" if point.is_infinity else f"{point.x},{point.y}"


def _solve_linear_congruence(coefficient: int, residue: int, modulo: int) -> list[int]:
    divisor = gcd(coefficient, modulo)
    if residue % divisor != 0:
        return []

    reduced_coefficient = coefficient // divisor
    reduced_residue = residue // divisor
    reduced_modulo = modulo // divisor
    if reduced_modulo == 1:
        return list(range(modulo))

    base_solution = (reduced_residue * mod_inverse(reduced_coefficient, reduced_modulo)) % reduced_modulo
    return sorted((base_solution + step * reduced_modulo) % modulo for step in range(divisor))


def _matching_discrete_log_candidates(generator: Point, target: Point, candidates: list[int]) -> list[int]:
    target_payload = target.to_payload()
    return [
        candidate
        for candidate in candidates
        if multiply_point_fast(candidate, generator).to_payload() == target_payload
    ]


def simulate_pollards_rho(
    generator: Point,
    secret_scalar: int,
    max_steps: int = 48,
) -> dict[str, object]:
    if max_steps < 1:
        raise EccDomainError("El número máximo de pasos debe ser positivo.")

    curve = generator.curve
    order = point_order(generator)
    target = multiply_point_fast(secret_scalar, generator)
    seen: dict[str, dict[str, object]] = {}
    steps: list[dict[str, object]] = []
    current = generator
    alpha = 1
    beta = 0
    collision: dict[str, object] | None = None

    for index in range(max_steps + 1):
        key = point_key(current)
        previous_step = seen.get(key)
        partition = 0 if current.is_infinity else (current.x or 0) % curve.p % 3
        step = {
            "index": index,
            "point": current.to_payload(),
            "alpha": alpha,
            "beta": beta,
            "action": "inicio" if index == 0 else "paso rho",
            "partition": partition,
        }
        steps.append(step)

        if previous_step is not None:
            alpha_delta = (int(previous_step["alpha"]) - alpha) % order
            beta_delta = (beta - int(previous_step["beta"])) % order
            candidates = _solve_linear_congruence(beta_delta, alpha_delta, order)
            valid_candidates = _matching_discrete_log_candidates(generator, target, candidates)
            recovered_secret = valid_candidates[0] if len(valid_candidates) == 1 else None
            collision = {
                "firstIndex": previous_step["index"],
                "secondIndex": index,
                "point": current.to_payload(),
                "alphaDelta": alpha_delta,
                "betaDelta": beta_delta,
                "recoveredSecret": recovered_secret,
                "candidateSecrets": valid_candidates,
                "note": (
                    "La colisión permite despejar k módulo n."
                    if recovered_secret is not None
                    else "Hay colisión, pero el denominador no es invertible módulo n."
                ),
            }
            break

        seen[key] = step

        if partition == 0:
            current = add_points_fast(current, generator)
            alpha = (alpha + 1) % order
        elif partition == 1:
            current = add_points_fast(current, current)
            alpha = (2 * alpha) % order
            beta = (2 * beta) % order
        else:
            current = add_points_fast(current, target)
            beta = (beta + 1) % order

    return {
        "target": target.to_payload(),
        "order": order,
        "steps": steps,
        "collision": collision,
    }


def simulate_baby_step_giant_step(generator: Point, secret_scalar: int) -> dict[str, object]:
    curve = generator.curve
    order = point_order(generator)
    if order < 2:
        raise EccDomainError("El punto base debe tener orden mayor que 1.")

    target = multiply_point_fast(secret_scalar, generator)
    m = math.ceil(math.sqrt(order))
    baby_steps: list[dict[str, object]] = []
    giant_steps: list[dict[str, object]] = []
    baby_map: dict[str, int] = {}
    baby = curve.point(None, None)

    for index in range(m):
        baby_steps.append({"index": index, "point": baby.to_payload()})
        baby_map.setdefault(point_key(baby), index)
        baby = add_points_fast(baby, generator)

    stride = multiply_point_fast(m, generator)
    inverse_stride = stride.negate()
    giant = target
    result: int | None = None

    for index in range(m + 1):
        matched_baby_index = baby_map.get(point_key(giant))
        item: dict[str, object] = {"index": index, "point": giant.to_payload()}
        if matched_baby_index is not None:
            item["matchedBabyIndex"] = matched_baby_index
            result = (index * m + matched_baby_index) % order
            giant_steps.append(item)
            break

        giant_steps.append(item)
        giant = add_points_fast(giant, inverse_stride)

    return {
        "order": order,
        "target": target.to_payload(),
        "m": m,
        "babySteps": baby_steps,
        "giantSteps": giant_steps,
        "result": result,
        "found": result is not None,
    }


def describe_point(point: Point) -> str:
    return format_point(point)

from __future__ import annotations

from .errors import EccDomainError


def mod(value: int, modulo: int) -> int:
    if modulo <= 0:
        raise EccDomainError("El módulo debe ser un entero positivo.")
    return value % modulo


def gcd(left: int, right: int) -> int:
    a = abs(left)
    b = abs(right)
    while b:
        a, b = b, a % b
    return a


def extended_gcd(left: int, right: int) -> tuple[int, int, int]:
    old_r, r = left, right
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return abs(old_r), old_s, old_t


def mod_inverse(value: int, modulo: int) -> int:
    if modulo <= 1:
        raise EccDomainError("El módulo debe ser mayor que 1.")

    normalized = value % modulo
    divisor, coefficient, _ = extended_gcd(normalized, modulo)
    if divisor != 1:
        raise EccDomainError(f"No existe inverso modular para {value} módulo {modulo}.")
    return coefficient % modulo


def is_prime(value: int) -> bool:
    n = int(value)
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    divisor = 5
    step = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += step
        step = 6 - step
    return True


def factor_integer(value: int) -> list[dict[str, int]]:
    remainder = abs(int(value))
    factors: list[dict[str, int]] = []

    if remainder < 2:
        return factors

    exponent = 0
    while remainder % 2 == 0:
        exponent += 1
        remainder //= 2
    if exponent:
        factors.append({"factor": 2, "exponent": exponent})

    divisor = 3
    while divisor * divisor <= remainder:
        exponent = 0
        while remainder % divisor == 0:
            exponent += 1
            remainder //= divisor
        if exponent:
            factors.append({"factor": divisor, "exponent": exponent})
        divisor += 2

    if remainder > 1:
        factors.append({"factor": remainder, "exponent": 1})

    return factors


def simple_hash_to_int(message: str, modulo: int) -> int:
    if modulo <= 0:
        raise EccDomainError("El módulo del hash debe ser positivo.")

    value = 0
    for char in message:
        value = ((value * 31) + ord(char)) & 0xFFFFFFFF
    return value % modulo

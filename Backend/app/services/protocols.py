from __future__ import annotations

from .elliptic_curve import Point, add_points_fast, multiply_point_fast, normalize_private_scalar, point_order
from .errors import EccDomainError
from .number_theory import gcd, mod_inverse, simple_hash_to_int


def simulate_ecdh(generator: Point, alice_secret: int, bob_secret: int) -> dict[str, object]:
    order = point_order(generator)
    alice_private = normalize_private_scalar(alice_secret, order)
    bob_private = normalize_private_scalar(bob_secret, order)

    alice_public = multiply_point_fast(alice_private, generator)
    bob_public = multiply_point_fast(bob_private, generator)
    shared_by_alice = multiply_point_fast(alice_private, bob_public)
    shared_by_bob = multiply_point_fast(bob_private, alice_public)

    return {
        "order": order,
        "alicePrivate": alice_private,
        "bobPrivate": bob_private,
        "alicePublic": alice_public.to_payload(),
        "bobPublic": bob_public.to_payload(),
        "sharedByAlice": shared_by_alice.to_payload(),
        "sharedByBob": shared_by_bob.to_payload(),
        "matches": shared_by_alice.to_payload() == shared_by_bob.to_payload(),
    }


def simulate_ecdsa(
    generator: Point,
    private_secret: int,
    nonce_start: int,
    message: str,
) -> dict[str, object]:
    order = point_order(generator)
    if order < 3:
        raise EccDomainError("El orden del generador debe ser al menos 3 para ECDSA.")

    private_key = normalize_private_scalar(private_secret, order)
    public_key = multiply_point_fast(private_key, generator)
    digest = simple_hash_to_int(message, order)
    start = normalize_private_scalar(nonce_start, order)

    for attempt in range(order * 2):
        nonce = normalize_private_scalar(start + attempt, order)
        if gcd(nonce, order) != 1:
            continue

        try:
            nonce_point = multiply_point_fast(nonce, generator)
            if nonce_point.is_infinity or nonce_point.x is None:
                continue

            r = nonce_point.x % order
            if r == 0:
                continue

            nonce_inverse = mod_inverse(nonce, order)
            s = (nonce_inverse * (digest + r * private_key)) % order
            if s == 0 or gcd(s, order) != 1:
                continue

            w = mod_inverse(s, order)
            u1 = (digest * w) % order
            u2 = (r * w) % order
            left = multiply_point_fast(u1, generator)
            right = multiply_point_fast(u2, public_key)
            validation_point = add_points_fast(left, right)
            valid = (
                not validation_point.is_infinity
                and validation_point.x is not None
                and validation_point.x % order == r
            )

            return {
                "order": order,
                "privateKey": private_key,
                "publicKey": public_key.to_payload(),
                "nonce": nonce,
                "hash": digest,
                "signature": {"r": r, "s": s},
                "verification": {
                    "u1": u1,
                    "u2": u2,
                    "point": validation_point.to_payload(),
                    "valid": valid,
                },
            }
        except EccDomainError:
            continue

    raise EccDomainError("No se encontró un nonce válido para esta curva didáctica.")

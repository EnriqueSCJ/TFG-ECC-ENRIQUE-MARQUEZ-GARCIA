from app.services.number_theory import gcd, is_prime, mod_inverse


def test_mod_inverse_satisfies_bezout_residue() -> None:
    inverse = mod_inverse(7, 19)
    assert (7 * inverse) % 19 == 1


def test_gcd_handles_negative_values() -> None:
    assert gcd(-84, 30) == 6


def test_is_prime_rejects_composites() -> None:
    assert is_prime(997)
    assert not is_prime(999)


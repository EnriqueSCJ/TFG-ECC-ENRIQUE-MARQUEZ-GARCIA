from app.services.attacks import simulate_baby_step_giant_step, simulate_pollards_rho
from app.services.elliptic_curve import Curve
from app.services.number_theory import gcd


def test_pollards_rho_recovers_secret_from_non_invertible_collision() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_pollards_rho(curve.point(0, 1), secret_scalar=5, max_steps=80)

    collision = result["collision"]

    assert collision is not None
    assert gcd(collision["betaDelta"], result["order"]) != 1
    assert collision["recoveredSecret"] == 5
    assert collision["candidateSecrets"] == [5]


def test_baby_step_giant_step_still_recovers_secret() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_baby_step_giant_step(curve.point(0, 1), secret_scalar=9)

    assert result["found"] is True
    assert result["result"] == 9

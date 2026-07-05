from fastapi.testclient import TestClient

from app.main import app
from app.services.elliptic_curve import Curve
from app.services.protocols import simulate_ecdh, simulate_ecdsa


client = TestClient(app)


def sample_parameters() -> dict[str, int | str]:
    return {
        "a": -1,
        "b": 1,
        "p": 17,
        "gx": 0,
        "gy": 1,
        "n": 14,
        "h": 1,
        "name": "E: y^2 = x^3 - x + 1",
    }


def test_ecdh_shared_secret_matches() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_ecdh(curve.point(0, 1), alice_secret=5, bob_secret=8)

    assert result["matches"] is True
    assert result["sharedByAlice"] == result["sharedByBob"]


def test_ecdh_returns_normalized_private_scalars_used_by_the_protocol() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_ecdh(curve.point(0, 1), alice_secret=27, bob_secret=-4)

    assert result["order"] == 14
    assert result["alicePrivate"] == 1
    assert result["bobPrivate"] == 9
    assert result["matches"] is True


def test_ecdsa_verification_is_valid_for_sample_domain() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_ecdsa(curve.point(3, 5), private_secret=1, nonce_start=1, message="ECC didáctico")

    assert result["verification"]["valid"] is True


def test_ecdsa_default_frontend_values_are_valid() -> None:
    curve = Curve(a=-1, b=1, p=17)
    result = simulate_ecdsa(curve.point(0, 1), private_secret=2, nonce_start=1, message="ECC didáctico")

    assert result["signature"] == {"r": 5, "s": 5}
    assert result["verification"]["valid"] is True


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_finite_points_endpoint_returns_discriminant_and_points() -> None:
    response = client.post("/ecc/finite-points", json=sample_parameters())

    assert response.status_code == 200
    payload = response.json()
    assert payload["discriminant"] == 6
    assert {"x": 0, "y": 1, "label": "(0, 1)"} in payload["points"]


def test_scalar_multiply_endpoint_returns_walk() -> None:
    response = client.post(
        "/ecc/scalar-multiply",
        json={
            "parameters": sample_parameters(),
            "point": {"x": 0, "y": 1, "label": "P"},
            "scalar": 9,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["x"] is not None
    assert payload["walk"][0]["point"]["label"] == "𝒪"


def test_group_add_endpoint_rejects_points_outside_curve() -> None:
    response = client.post(
        "/ecc/group/add",
        json={
            "parameters": sample_parameters(),
            "left": {"x": 2, "y": 2},
            "right": {"x": 0, "y": 1},
        },
    )

    assert response.status_code == 422
    assert "no pertenece a la curva" in response.json()["detail"]


def test_schema_rejects_unexpected_curve_fields() -> None:
    payload = {**sample_parameters(), "unexpected": 1}
    response = client.post("/ecc/finite-points", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"] == "Parámetros de entrada no válidos."


def test_curve_metadata_endpoint_rejects_zero_cofactor() -> None:
    payload = {**sample_parameters(), "h": 0}
    response = client.post("/ecc/finite-points", json=payload)

    assert response.status_code == 422
    assert "cofactor" in response.json()["detail"]


def test_curve_metadata_endpoint_rejects_zero_declared_order() -> None:
    payload = {**sample_parameters(), "n": 0}
    response = client.post("/ecc/finite-points", json=payload)

    assert response.status_code == 422
    assert "orden n" in response.json()["detail"]

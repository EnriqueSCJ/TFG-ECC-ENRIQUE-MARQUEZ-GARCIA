import pytest

from app.services.elliptic_curve import (
    Curve,
    Point,
    add_points,
    add_points_fast,
    curve_group_order,
    finite_curve_points,
    multiply_point,
    multiply_point_fast,
    point_order,
)
from app.services.errors import EccDomainError


def sample_curve() -> Curve:
    return Curve(a=-1, b=1, p=17, gx=0, gy=1, n=14, h=1)


def all_group_points(curve: Curve) -> list[Point]:
    return [curve.point(None, None)] + [
        curve.point(int(point["x"]), int(point["y"])) for point in finite_curve_points(curve)
    ]


def add(curve: Curve, left: Point, right: Point) -> Point:
    result = add_points(left, right)["result"]
    return curve.point(result["x"], result["y"])


def test_finite_points_belong_to_curve() -> None:
    curve = sample_curve()
    for point in finite_curve_points(curve):
        assert curve.contains_coordinates(int(point["x"]), int(point["y"]))


def test_group_addition_known_result() -> None:
    curve = sample_curve()
    left = curve.point(0, 1)
    right = curve.point(1, 1)

    result = add_points(left, right)["result"]

    assert result["x"] == 16
    assert result["y"] == 16


def test_fast_group_addition_matches_explanatory_operation_for_every_pair() -> None:
    curve = sample_curve()
    points = all_group_points(curve)

    for left in points:
        for right in points:
            explanatory_result = add_points(left, right)["result"]
            assert add_points_fast(left, right).to_payload() == curve.point(**explanatory_result).to_payload()


def test_identity_and_inverse_hold_for_every_group_point() -> None:
    curve = sample_curve()
    identity = curve.point(None, None)

    for point in all_group_points(curve):
        assert add(curve, identity, point).to_payload() == point.to_payload()
        assert add(curve, point, identity).to_payload() == point.to_payload()
        assert add(curve, point, point.negate()).is_infinity


def test_group_addition_is_associative_on_sample_curve() -> None:
    curve = sample_curve()
    points = all_group_points(curve)

    for left in points:
        for middle in points:
            for right in points:
                left_associated = add(curve, add(curve, left, middle), right)
                right_associated = add(curve, left, add(curve, middle, right))
                assert left_associated.to_payload() == right_associated.to_payload()


def test_scalar_multiplication_matches_repeated_addition() -> None:
    curve = sample_curve()
    point = curve.point(0, 1)
    current = curve.point(None, None)

    for _ in range(9):
        current = curve.point(**add_points(current, point)["result"])

    result = multiply_point(9, point)["result"]

    assert result == current.to_payload()


def test_jacobian_scalar_multiplication_matches_public_result_for_many_scalars() -> None:
    curve = sample_curve()
    point = curve.point(0, 1)

    for scalar in range(-30, 31):
        public_result = multiply_point(scalar, point)["result"]
        fast_result = multiply_point_fast(scalar, point)
        assert fast_result.to_payload() == public_result


def test_jacobian_scalar_multiplication_matches_repeated_addition_for_every_point() -> None:
    for curve in [sample_curve(), Curve(a=2, b=2, p=17)]:
        for point in all_group_points(curve):
            current = curve.point(None, None)
            for scalar in range(0, 24):
                assert multiply_point_fast(scalar, point).to_payload() == current.to_payload()
                current = add(curve, current, point)


def test_generator_order_is_detected() -> None:
    curve = sample_curve()
    assert point_order(curve.point(0, 1)) == 14


def test_point_order_is_reduced_from_group_order_factors() -> None:
    curve = sample_curve()

    assert curve_group_order(curve) == 14
    assert point_order(curve.point(0, 1)) == 14
    assert point_order(curve.point(3, 5)) == 7
    assert point_order(curve.point(12, 0)) == 2


@pytest.mark.parametrize(
    ("a", "b", "p"),
    [
        (0, 0, 17),
        (-1, 1, 21),
        (-1, 1, 3),
    ],
)
def test_curve_rejects_invalid_domains(a: int, b: int, p: int) -> None:
    with pytest.raises(EccDomainError):
        Curve(a=a, b=b, p=p)


@pytest.mark.parametrize(
    "metadata",
    [
        {"n": 0},
        {"n": -7},
        {"h": 0},
        {"h": -1},
    ],
)
def test_curve_rejects_invalid_subgroup_metadata(metadata: dict[str, int]) -> None:
    with pytest.raises(EccDomainError):
        Curve(a=-1, b=1, p=17, **metadata)

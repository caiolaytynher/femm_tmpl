import pytest
from src.mathlib.vector2 import DOWN, LEFT, RIGHT, UP, ZERO, Vector2


@pytest.fixture
def v() -> Vector2:
    return Vector2(3, 4)


def test_iter(v: Vector2) -> None:
    assert len(v) == 2
    for n, expected_n in zip(v, [v.x, v.y], strict=False):
        assert n == expected_n


def test_parse(v: Vector2) -> None:
    assert Vector2.parse((v.x, v.y)) == v
    assert Vector2.parse([v.x, v.y]) == v


def test_addition(v: Vector2) -> None:
    assert v + v == Vector2(2 * v.x, 2 * v.y)
    assert v + (v.x, v.y) == Vector2(2 * v.x, 2 * v.y)
    assert v + [v.x, v.y] == Vector2(2 * v.x, 2 * v.y)


def test_subtraction(v: Vector2) -> None:
    assert v - v == ZERO
    assert v - (v.x, v.y) == ZERO
    assert v - [v.x, v.y] == ZERO


def test_scalar_multiplication(v: Vector2) -> None:
    assert -v == Vector2(-v.x, -v.y)
    assert v * 2 == Vector2(2 * v.x, 2 * v.y)


def test_scalar_division(v: Vector2) -> None:
    assert v / 1 == v
    assert v / 2 == Vector2(v.x / 2, v.y / 2)


def test_magnitude_and_direction(v: Vector2) -> None:
    assert v.direction().magnitude() == 1


def test_distance(v: Vector2) -> None:
    assert Vector2.distance(v, v) == 0
    assert Vector2.distance(v, v * 2) == v.magnitude()
    assert Vector2.distance(v, (v.x, v.y + 2)) == 2
    assert Vector2.distance(v, (v.x + 2, v.y)) == 2
    assert Vector2.distance(v, (v.x + 3, v.y + 4)) == 5


def test_midpoint(v: Vector2) -> None:
    assert Vector2.midpoint(v, v) == v
    assert Vector2.midpoint(v, (v.x, v.y + 2)) == Vector2(v.x, v.y + 1)
    assert Vector2.midpoint(v, (v.x + 2, v.y)) == Vector2(v.x + 1, v.y)
    assert Vector2.midpoint(v, (v.x + 2, v.y + 2)) == Vector2(v.x + 1, v.y + 1)


def test_dot_product(v: Vector2) -> None:
    assert Vector2.dot(v, v) == v.magnitude() ** 2
    assert Vector2.dot(v, UP) == v.y
    assert Vector2.dot(v, DOWN) == -v.y
    assert Vector2.dot(v, LEFT) == -v.x
    assert Vector2.dot(v, RIGHT) == v.x
    assert Vector2.dot(v, v.perpendicular()) == 0
    assert Vector2.dot(v, v.perpendicular('counterclockwise')) == 0

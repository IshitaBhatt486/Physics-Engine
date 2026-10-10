import pytest

from physics_engine.entities import Ball


def test_ball_mass_is_proportional_to_area() -> None:
    ball = Ball(0, 0, 4, (255, 255, 255))
    assert ball.mass == 16


def test_ball_rejects_non_positive_radius() -> None:
    with pytest.raises(ValueError):
        Ball(0, 0, 0, (255, 255, 255))


def test_contains_point() -> None:
    ball = Ball(10, 10, 5, (255, 255, 255))
    assert ball.contains_point((13, 14))
    assert not ball.contains_point((16, 10))

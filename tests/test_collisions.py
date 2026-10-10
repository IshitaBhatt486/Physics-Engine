from physics_engine.entities import Ball
from physics_engine.physics import resolve_collisions


def test_head_on_equal_mass_collision_exchanges_direction() -> None:
    first = Ball(100, 100, 10, (0, 0, 0), vx=4)
    second = Ball(119, 100, 10, (0, 0, 0), vx=-4)
    resolve_collisions([first, second])
    assert first.vx < 0
    assert second.vx > 0
    assert second.x - first.x >= 20


def test_coincident_balls_do_not_crash() -> None:
    first = Ball(100, 100, 10, (0, 0, 0))
    second = Ball(100, 100, 10, (0, 0, 0))
    resolve_collisions([first, second])
    assert first.x != second.x

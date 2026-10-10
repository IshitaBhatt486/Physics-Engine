from physics_engine.config import HEIGHT, WIDTH
from physics_engine.entities import Ball
from physics_engine.physics import resolve_wall_collision


def test_right_wall_keeps_ball_in_bounds_and_reverses_velocity() -> None:
    ball = Ball(WIDTH - 5, 100, 10, (0, 0, 0), vx=3)
    resolve_wall_collision(ball)
    assert ball.x == WIDTH - ball.radius
    assert ball.vx < 0


def test_floor_keeps_ball_in_bounds() -> None:
    ball = Ball(100, HEIGHT, 10, (0, 0, 0), vy=3)
    resolve_wall_collision(ball)
    assert ball.y == HEIGHT - ball.radius
    assert ball.vy < 0

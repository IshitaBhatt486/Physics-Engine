"""Deterministic, renderer-independent 2D circle physics."""

from collections.abc import Iterable
import math

from .config import COLLISION_DAMPING, FRICTION, GRAVITY, HEIGHT, WALL_ELASTICITY, WIDTH
from .entities import Ball


def advance_ball(ball: Ball, dt: float) -> None:
    """Advance one ball by ``dt`` seconds using a 60 FPS reference scale."""
    if ball.is_dragging:
        return

    frame_scale = dt * 60.0
    ball.vy += GRAVITY * frame_scale
    damping = FRICTION**frame_scale
    ball.vx *= damping
    ball.vy *= damping
    ball.x += ball.vx * frame_scale
    ball.y += ball.vy * frame_scale
    resolve_wall_collision(ball)


def resolve_wall_collision(ball: Ball) -> None:
    """Keep a ball inside the window and apply wall restitution."""
    if ball.x + ball.radius > WIDTH:
        ball.x = WIDTH - ball.radius
        ball.vx = -abs(ball.vx) * WALL_ELASTICITY
    elif ball.x - ball.radius < 0:
        ball.x = ball.radius
        ball.vx = abs(ball.vx) * WALL_ELASTICITY

    if ball.y + ball.radius > HEIGHT:
        ball.y = HEIGHT - ball.radius
        ball.vy = -abs(ball.vy) * WALL_ELASTICITY
        if abs(ball.vy) < GRAVITY * 2:
            ball.vy = 0.0
    elif ball.y - ball.radius < 0:
        ball.y = ball.radius
        ball.vy = abs(ball.vy) * WALL_ELASTICITY


def resolve_collisions(balls: Iterable[Ball]) -> None:
    """Resolve pairwise overlaps and damped elastic velocity exchanges."""
    bodies = list(balls)
    for index, first in enumerate(bodies):
        for second in bodies[index + 1 :]:
            _resolve_pair(first, second)


def _resolve_pair(first: Ball, second: Ball) -> None:
    dx = second.x - first.x
    dy = second.y - first.y
    distance_squared = dx * dx + dy * dy
    minimum_distance = first.radius + second.radius
    if distance_squared >= minimum_distance * minimum_distance:
        return

    if distance_squared == 0:
        nx, ny, distance = 1.0, 0.0, 0.0
    else:
        distance = math.sqrt(distance_squared)
        nx, ny = dx / distance, dy / distance

    overlap = minimum_distance - distance
    total_mass = first.mass + second.mass
    first.x -= nx * overlap * (second.mass / total_mass)
    first.y -= ny * overlap * (second.mass / total_mass)
    second.x += nx * overlap * (first.mass / total_mass)
    second.y += ny * overlap * (first.mass / total_mass)

    relative_normal_velocity = (second.vx - first.vx) * nx + (second.vy - first.vy) * ny
    if relative_normal_velocity >= 0:
        return
    impulse = -(1 + COLLISION_DAMPING) * relative_normal_velocity
    impulse /= (1 / first.mass) + (1 / second.mass)
    impulse_x, impulse_y = impulse * nx, impulse * ny
    first.vx -= impulse_x / first.mass
    first.vy -= impulse_y / first.mass
    second.vx += impulse_x / second.mass
    second.vy += impulse_y / second.mass

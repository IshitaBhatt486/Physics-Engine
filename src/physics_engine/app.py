"""Pygame application entry point."""

import random

import pygame

from .config import BLUE, FPS, HEIGHT, WIDTH
from .entities import Ball
from .physics import advance_ball, resolve_collisions
from .ui import Button, draw_background, draw_ball, draw_controls_overlay, draw_pause_overlay, draw_status, draw_toolbar


def create_random_ball() -> Ball:
    radius = random.randint(15, 35)
    return Ball(
        x=random.randint(radius + 50, WIDTH - radius - 50),
        y=random.randint(max(radius + 90, 110), 300),
        radius=radius,
        color=tuple(random.randint(50, 255) for _ in range(3)),
        vx=random.choice([-5, -4, -3, 3, 4, 5]),
        vy=random.choice([-5, -4, -3, 3, 4, 5]),
    )


def initial_scene() -> list[Ball]:
    """Create a fresh scene without coupling reset behaviour to the UI."""
    return [Ball(400, 200, 30, BLUE, vx=3, vy=-3)]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics Engine")
    clock = pygame.time.Clock()
    status_font = pygame.font.SysFont("Segoe UI", 16, bold=True)
    overlay_font = pygame.font.SysFont("Segoe UI", 42, bold=True)
    controls_font = pygame.font.SysFont("Segoe UI", 18)
    buttons = [
        Button(18, 20, 100, 36, "Add ball", (43, 150, 89)),
        Button(128, 20, 88, 36, "Reset", (66, 105, 190)),
        Button(226, 20, 90, 36, "Pause", (179, 119, 43)),
        Button(326, 20, 64, 36, "Clear", (172, 71, 76)),
        Button(400, 20, 36, 36, "?", (99, 86, 174)),
    ]
    balls = initial_scene()
    dragged_ball: Ball | None = None
    paused = False
    show_onboarding = True
    show_controls = False
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_onboarding = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_a:
                    balls.append(create_random_ball())
                elif event.key == pygame.K_r:
                    balls, dragged_ball = initial_scene(), None
                elif event.key == pygame.K_c:
                    balls.clear()
                    dragged_ball = None
                continue

            button_actions = [button.handle_event(event) for button in buttons]
            if any(button_actions):
                if button_actions[0]:
                    balls.append(create_random_ball())
                elif button_actions[1]:
                    balls, dragged_ball = initial_scene(), None
                elif button_actions[2]:
                    paused = not paused
                elif button_actions[3]:
                    balls.clear()
                    dragged_ball = None
                elif button_actions[4]:
                    show_controls = not show_controls
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ball in reversed(balls):
                    if ball.contains_point(event.pos):
                        ball.is_dragging = True
                        dragged_ball = ball
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragged_ball:
                dragged_ball.is_dragging = False
                dragged_ball = None
            elif event.type == pygame.MOUSEMOTION and dragged_ball:
                dragged_ball.x, dragged_ball.y = event.pos
                dragged_ball.vx, dragged_ball.vy = event.rel

        if not paused:
            for ball in balls:
                advance_ball(ball, dt)
            resolve_collisions(balls)

        draw_background(screen)
        for ball in balls:
            draw_ball(screen, ball)
        draw_toolbar(screen, buttons)
        draw_status(screen, status_font, len(balls), clock.get_fps(), paused)
        if paused:
            draw_pause_overlay(screen, overlay_font)
        if show_onboarding or show_controls:
            draw_controls_overlay(screen, overlay_font, controls_font, show_onboarding)
        pygame.display.flip()

    pygame.quit()

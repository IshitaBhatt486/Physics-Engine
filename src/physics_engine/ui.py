"""Pygame user-interface and drawing components."""

import pygame

from .entities import Ball

Color = tuple[int, int, int]


class Button:
    """A small, self-contained toolbar button."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Color) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self._pressed = False
        self._font = pygame.font.SysFont("Segoe UI", 16, bold=True)

    def draw(self, surface: pygame.Surface) -> None:
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        main = tuple(min(255, channel + 24) for channel in self.color) if hovered else self.color
        shadow = tuple(max(0, channel - 55) for channel in self.color)
        draw_rect = self.rect.move(0, 2 if self._pressed else 0)
        pygame.draw.rect(surface, shadow, self.rect.move(0, 3), border_radius=8)
        pygame.draw.rect(surface, main, draw_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), draw_rect, width=1, border_radius=8)
        label = self._font.render(self.text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=draw_rect.center))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True only for a complete click within the button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._pressed = self.rect.collidepoint(event.pos)
            return False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = self._pressed and self.rect.collidepoint(event.pos)
            self._pressed = False
            return clicked
        return False


def draw_background(surface: pygame.Surface) -> None:
    """Draw a subtle grid without making the simulation area distracting."""
    surface.fill((13, 18, 30))
    grid_color = (24, 33, 50)
    for x in range(0, surface.get_width(), 40):
        pygame.draw.line(surface, grid_color, (x, 0), (x, surface.get_height()))
    for y in range(0, surface.get_height(), 40):
        pygame.draw.line(surface, grid_color, (0, y), (surface.get_width(), y))


def draw_toolbar(surface: pygame.Surface, buttons: list[Button]) -> None:
    pygame.draw.rect(surface, (25, 34, 52), (0, 0, surface.get_width(), 76))
    pygame.draw.line(surface, (70, 88, 116), (0, 76), (surface.get_width(), 76))
    for button in buttons:
        button.draw(surface)


def draw_status(surface: pygame.Surface, font: pygame.font.Font, ball_count: int, fps: float, paused: bool) -> None:
    state = "PAUSED" if paused else "RUNNING"
    state_color = (255, 205, 80) if paused else (105, 230, 155)
    status = font.render(f"{state} | {ball_count} balls", True, state_color)
    surface.blit(status, (450, 28))
    fps_text = font.render(f"{fps:4.0f} FPS", True, (220, 230, 245))
    surface.blit(fps_text, fps_text.get_rect(topright=(surface.get_width() - 24, 28)))


def draw_pause_overlay(surface: pygame.Surface, font: pygame.font.Font) -> None:
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((4, 8, 18, 125))
    surface.blit(overlay, (0, 0))
    message = font.render("PAUSED", True, (255, 255, 255))
    surface.blit(message, message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))


def draw_controls_overlay(surface: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font, onboarding: bool) -> None:
    """Draw the onboarding/help panel without affecting simulation state."""
    dimmer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    dimmer.fill((4, 8, 18, 175))
    surface.blit(dimmer, (0, 0))
    panel = pygame.Rect(0, 0, 480, 300)
    panel.center = (surface.get_width() // 2, surface.get_height() // 2)
    pygame.draw.rect(surface, (28, 40, 62), panel, border_radius=16)
    pygame.draw.rect(surface, (116, 147, 195), panel, width=2, border_radius=16)
    title = "Welcome to Physics Engine" if onboarding else "Controls"
    title_surface = title_font.render(title, True, (245, 249, 255))
    surface.blit(title_surface, title_surface.get_rect(center=(panel.centerx, panel.y + 43)))

    lines = [
        "Add a ball     Click Add ball or press A",
        "Move a ball    Click, drag, and release it",
        "Pause          Click Pause or press Space",
        "Reset          Click Reset or press R",
        "Clear          Click Clear or press C",
    ]
    for index, line in enumerate(lines):
        line_surface = body_font.render(line, True, (207, 220, 240))
        surface.blit(line_surface, (panel.x + 42, panel.y + 83 + index * 31))

    footer = "Click anywhere to begin" if onboarding else "Click ? again to close"
    footer_surface = body_font.render(footer, True, (130, 220, 175))
    surface.blit(footer_surface, footer_surface.get_rect(center=(panel.centerx, panel.bottom - 33)))


def draw_ball(surface: pygame.Surface, ball: Ball) -> None:
    center = (round(ball.x), round(ball.y))
    radius = round(ball.radius)
    pygame.draw.circle(surface, (3, 7, 14), (center[0] + 3, center[1] + 4), radius)
    pygame.draw.circle(surface, ball.color, center, radius)
    pygame.draw.circle(surface, (225, 235, 255), center, radius, width=1)
    pygame.draw.circle(surface, (255, 255, 255), (center[0] - radius // 3, center[1] - radius // 3), max(2, radius // 4))

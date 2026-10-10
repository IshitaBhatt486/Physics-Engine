"""Simulation entities independent of Pygame rendering."""

from dataclasses import dataclass, field


Color = tuple[int, int, int]


@dataclass
class Ball:
    """A circular body whose mass is proportional to its area."""

    x: float
    y: float
    radius: float
    color: Color
    vx: float = 0.0
    vy: float = 0.0
    is_dragging: bool = False
    mass: float = field(init=False)

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Ball radius must be positive.")
        self.mass = self.radius**2

    def contains_point(self, position: tuple[float, float]) -> bool:
        """Return whether a screen-space point lies inside this ball."""
        dx = position[0] - self.x
        dy = position[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius

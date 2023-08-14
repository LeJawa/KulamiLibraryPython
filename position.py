"""Position class for the game."""

from cmath import sqrt
from dataclasses import dataclass


@dataclass
class Position:
    """Position class for the game."""

    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def distance_from(self, other: "Position") -> float:
        """Calculate the distance between two positions."""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2).real

    def is_negative(self) -> bool:
        """Check if the position is negative."""
        return self.x < 0 or self.y < 0

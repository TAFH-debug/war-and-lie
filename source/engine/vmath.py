from math import pi, sqrt
from typing import Callable


class Vector2d:
    """
    Class to represent a pair of floats.
    """

    x: float
    y: float

    def __init__(self, a: float = 0, b: float = 0):
        self.x = a
        self.y = b

    @staticmethod
    def from_tuple(tpl: tuple[float, float]) -> "Vector2d":
        return Vector2d(tpl[0], tpl[1])

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def distance(self, other: "Vector2d") -> float:
        return sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2))

    def intx(self) -> int:
        return int(self.x)

    def inty(self) -> int:
        return int(self.y)

    def distanceLooped(self, other: "Vector2d", size: "Vector2d") -> float:
        return sqrt(((self.x - other.x) ** 2) % ((size.x // 2) ** 2) + ((self.y - other.y) ** 2) % ((size.y // 2) ** 2))

    def __add__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector2d(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Vector2d(self.x / other, self.y / other)

    def operation(self, other: "Vector2d", operation: Callable[[float, float], float]) -> "Vector2d":
        return Vector2d(operation(self.x, other.x), operation(self.y, other.y))

    def __repr__(self) -> str:  # for debugging
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    def __eq__(self, other: "Vector2d") -> bool:
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other: "Vector2d") -> bool:
        return (self.x != other.x or self.y != other.y)


class Angle:
    """
    class that represent angles in radians
    """

    angle: float

    def __init__(self, angle: float = 0) -> None:
        self.angle = angle
        self.bound()

    def set(self, angle: float, isDeegre: bool = False):
        if isDeegre:
            angle = angle * pi / 180
        self.angle = angle
        self.bound()

    def get(self, isDeegre: bool = False):
        if isDeegre:
            return self.angle * 180 / pi
        return self.angle

    def bound(self):
        self.angle %= (2 * pi)

    def __add__(self, other: "Angle") -> "Angle":
        return Angle(self.get() + other.get())

    def __sub__(self, other: "Angle") -> "Angle":
        return Angle(self.get() - other.get())

    def __repr__(self) -> str:
        return str(self.angle)

    def __float__(self) -> float:
        return self.angle

from math import pi
from typing import Callable

class DoubleNumber[T]:
    """
    Class to represent pair of numbers.
    """
    
    x: T
    y: T
    
    def __init__(self, a: T, b: T):
        self.x = a
        self.y = b
    
    @staticmethod
    def from_tuple(tpl: tuple[T, T]) -> "DoubleNumber":
        return DoubleNumber(tpl[0], tpl[1])
    
    def as_tuple(self) -> tuple[T]:
        return self.x, self.y
    
    def __add__(self, other: "DoubleNumber[T]") -> "DoubleNumber[T]":
        return DoubleNumber(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "DoubleNumber[T]") -> "DoubleNumber[T]":
        return DoubleNumber(self.x - other.x, self.y - other.y)
    
    def operation(self, other: "DoubleNumber[T]", operation: Callable[[int, int], int]) -> "DoubleNumber[T]":
        return DoubleNumber(operation(self.x, other.x), operation(self.y, other.y))
    
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
        return Angle(self.get()+other.get())
    
    def __add__(self, other: int) -> "Angle":
        return Angle(self.get()+other)
    
    def __sub__(self, other: "Angle") -> "Angle":
        return Angle(self.get()-other.get())
    
    def __sub__(self, other: int) -> "Angle":
        return Angle(self.get()-other)
    
    def __repr__(self) -> str:
        return str(self.angle)

    def __float__(self) -> float:
        return self.angle

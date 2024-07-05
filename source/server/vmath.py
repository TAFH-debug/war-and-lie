from math import pi, sqrt, sin, cos, atan2
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
        return sqrt(((self.x - other.x + size.x / 2) % size.x - (size.x / 2)) ** 2 + ((self.y - other.y + size.y / 2) % size.y - (size.y / 2)) ** 2)

    def toAngle(self) -> "Angle":
        return Angle(atan2(-self.y, self.x))

    def __add__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector2d(self.x * other, self.y * other)
    
    def complexMultiply(self, other: "Vector2d") -> "Vector2d":
        # complex multiplying
        return Vector2d(self.x * other.x - self.y * other.y, self.y * other.x + self.x * other.y)

    def __truediv__(self, other: float):
        return Vector2d(self.x / other, self.y / other)

    def __floordiv__(self, other: float):
        return Vector2d(self.x // other, self.y // other)
    
    def __mod__(self, other: float):
        return Vector2d(self.x % other, self.y % other)

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

    def toVector2D(self) -> Vector2d:
        return Vector2d(cos(self.angle), sin(self.angle))

    def __add__(self, other: "Angle") -> "Angle":
        return Angle(self.get() + other.get())

    def __sub__(self, other: "Angle") -> "Angle":
        return Angle(self.get() - other.get())

    def __repr__(self) -> str:
        return str(self.angle)

    def __float__(self) -> float:
        return self.angle

class Mod4:
    def __init__(self, value: int = 0) -> None:
        self.value = value % 4
    
    def __add__(self, other: "Mod4") -> "Mod4":
        return Mod4((self.value + other.value) % 4)
    
    def __sub__(self, other: "Mod4") -> "Mod4":
        return Mod4((self.value - other.value) % 4)

    def __repr__(self) -> str:
        return self.value.__repr__()

    def __eq__(self, other: "Mod4") -> bool:
        return self.other == other.other

    def __ne__(self, other: "Mod4") -> bool:
        return self.other != other.other

class Direction(Mod4):
    def __init__(self, value: int = 0) -> None:
        super().__init__(value)
    
    def toAngle(self) -> Angle:
        return Angle(self.value * pi / 2)

    @staticmethod
    def fromAngle(ang: Angle) -> "Direction":
        return Direction((ang.get() + pi/4) // (pi/2))
    
    def toVector2d(self) -> Vector2d:
        return Directions.AsVector2D[self.value]

    @staticmethod
    def fromVector2d(ang: Vector2d) -> "Direction":
        newang = ang.complexMultiply(Vector2d(1, 1))
        return Direction(int(newang.y < 0) * 2 + int(newang.x < 0))

    def rotateVector2d(self, vec: Vector2d) -> Vector2d:
        return vec.complexMultiply(self.toVector2d())
    
class Directions:
    RIGHT = Direction(0)
    UP = Direction(1)
    LEFT = Direction(2)
    DOWN = Direction(3)
    
    AsVector2D = (
        Vector2d(1, 0), 
        Vector2d(0, -1), 
        Vector2d(-1, 0), 
        Vector2d(0, 1)
    )

def to_bytes(x) -> bytes:
    '''
    turns integers, floats into 4 length bytearray.\n
    float is rounded.\n
    lists are encoded badly
    '''
    if type(x) == int:
        res = bytearray(5)
        res[0] = 0
        for i in range(4):
            res[4-i] = (x // (256 ** i)) % 256
    elif type(x) == float:
        res = bytearray(5)
        res[0] = 1
        for i in range(4):
            res[4-i] = int((x // (256 ** (i - 2))) % 256)
    elif type(x) == bool:
        res = bytes((2, int(x)))
    elif type(x) in (tuple, list):
        res = bytearray(2)
        res[0] = 3
        n = 0
        for item in x:
            if type(item) in (int, float):
                res.extend(to_bytes(item))
                n += 5
            elif type(item) == bool:
                res.extend(to_bytes(item))
                n += 2
            elif type(item) in (tuple, list):
                ext = to_bytes(item)
                res.extend(ext)
                n += ext[1] + 2
            else:
                raise Exception(f"{type(item)}({item}) is not alowed")
        res[1] = n
    return bytes(res)

def from_bytes(x : bytes):
    if x[0] == 0:
        res = 0
        for i in range(4):
            res += x[4-i] * (256 ** i)
    elif x[0] == 1:
        res = 0
        for i in range(4):
            res += x[4-i] * (256 ** (i - 2))
    elif x[0] == 2:
        res = bool(x[1])
    elif x[0] == 3:
        res = []
        n = x[1]
        curr = 2
        while curr != n + 2:
            if x[curr] in (0, 1):
                res.append(from_bytes(x[curr: curr + 5]))
                curr += 5
            elif x[curr] == 2:
                res.append(from_bytes(x[curr: curr + 2]))
                curr += 2
            elif x[curr] == 3:
                res.append(from_bytes(x[curr: curr + x[curr + 1] + 2]))
                curr += x[curr + 1] + 2
            
    return res


a = [[2**i * 3**j for i in range(5)] for j in range(5)]

print((from_bytes(to_bytes(a))))
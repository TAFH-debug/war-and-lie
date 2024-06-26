from typing import Iterable

from server.vmath import *


# Needed for hp (or other things that have max value and are positive only)
class Alive:

    def __init__(self, maxValue: int, value: int | None = None):
        self.value: int = value or maxValue
        self.maxValue: int = maxValue

    # increase value and border it by max value
    def regenerate(self, value: int) -> None:
        self.value = min(self.value + value, self.maxValue)

    # decreases value and checks if it is positive
    def gainDamage(self, value: int) -> bool:
        self.value -= value
        return self.isAlive()

    # checks if it is positive
    def isAlive(self) -> bool:
        return self.value > 0

    # makes it easy to access to value (use " a() ")
    def __call__(self) -> int:
        return self.value


class Damage:
    damage: list[int]

    def __init__(self, damage: Iterable[int]) -> None:
        self.damage = list(damage)

    def __getitem__(self, index: int) -> int:
        return self.damage[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.damage[index] = value


class AliveInArmor(Alive):
    armorType: int
    armor: int

    def __init__(self, armorType: int, armor: int, maxValue: int, value: int | None = None) -> None:
        super().__init__(maxValue, value)
        self.armorType = armorType
        self.armor = armor

    def gainDamage(self, damage: Damage) -> bool:
        return super().gainDamage(damage[self.armorType] * (100 - self.armor) // 100)


# for money, resources and so on
class CountAble:
    def __init__(self, value: int, income: int):
        self.value = value
        self.income = income

    # changes value. change can be negative also
    def change(self, value: int | None = None):
        if value == None:
            self.value += self.income
        else:
            self.value = value


# generic class for all objects that has position
class GenericObject:
    pos: Vector2d
    size: Vector2d
    angle: Angle

    def __init__(self) -> None:
        self.pos = Vector2d(0, 0)
        self.size = Vector2d(1, 1)
        self.angle = Angle(0)

    def getRelatedCords(self, size: Vector2d) -> list[Vector2d]:
        delta = [
            Vector2d(-1, -1),
            Vector2d(0, -1),
            Vector2d(1, -1),
            Vector2d(1, 0),
            Vector2d(1, 1),
            Vector2d(0, 1),
            Vector2d(-1, 1),
            Vector2d(-1, 0)
        ]
        result = []
        for d in range(8):
            # TODO it should be voted for cycled or bordered map
            result.append((self.pos + delta[d]).operation(size, lambda a, b: a % b))
        return result



class GenericAliveObject(GenericObject, AliveInArmor):
    velocity: Vector2d

    def __init__(self, maxhp: int, armorType: int, armor: int, hp: int = None) -> None:
        GenericObject.__init__(self)
        AliveInArmor.__init__(self, armorType, armor, maxhp, hp)


class GenericMap[T]:
    size: Vector2d
    Map: list[list[T]]

    def __init__(self, size: Vector2d) -> None:
        self.size = size

    def __getitem__(self, index: int) -> list[T]:
        return self.Map[index]

    def get(self, pos: Vector2d) -> T:
        return self.Map[pos.inty()][pos.intx()]

    def initEmpty(self) -> None:
        self.Map = [[
            T(x, y) 
            for x in range(self.size.intx())] 
            for y in range(self.size.inty())]
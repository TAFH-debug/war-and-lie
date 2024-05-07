from source.textures import Texture
from .generic import GenericAliveObject, AliveInArmor, Damage
from .textures import *
from .util import *

class UnitType:
    texture: Texture
    size: DoubleNumber[int, int]
    speed: float
    hp: AliveInArmor
    damage: Damage

    def __init__(self, texture: Texture, size: DoubleNumber[int, int], speed: float, hp: AliveInArmor, damage: tuple[int, int, int]) -> None:
        self.texture = texture
        self.size = size
        self.speed = speed
        self.hp = hp
        self.damage = damage

class UnitTypes():
    """
    Here must be all unit types in the game
    """

    ship = UnitType(Textures.ship, (2, 2), 20, AliveInArmor(2, 10, 100), Damage((10, 23, 20)))

class Unit(GenericAliveObject):
    speed: float
    damage: Damage

    def __init__(self, unitType: UnitType, pos: DoubleNumber[int, int], size: DoubleNumber[int, int], direction: Angle, speed: float, damage: Damage) -> None:
        super().__init__(unitType.texture, unitType.hp(), unitType.hp.armorType, unitType.hp.armor)
        self.pos = pos
        self.size = size
        self.direction = direction
        self.speed = speed
        self.damage = damage
        # TODO tile where unit stands have to be indicated as taken
    
    def move(self):# TODO for talim and bfs for path finding.
        pass

    
from server.vmath import *
from .generic import GenericObject, Damage
from math import atan2

class WeaponType:
    id: str
    damage: Damage
    rapidity: int # ticks between series
    shootSeries: int # how much shoots in series
    canAttack: tuple[bool]
    distance: float
    fov: Angle

    def __init__(self,id: str = "wal:weapon:none", damage: Damage = Damage((0, 0, 0)), rapidity: int = 0, shootSeries: int = 0, canAttack: tuple[bool] = (0, 0, 0, 0, 0), distance: float = 0, fov: Angle = Angle(0)) -> None:
        self.damage = damage
        self.rapidity = rapidity
        self.shootSeries = shootSeries
        self.canAttack = canAttack
        self.distance = distance
        self.fov = fov

class Weapon(GenericObject):
    weaponType: WeaponType
    reloading: int

    def __init__(self, weaponType: WeaponType, pos: Vector2d, angle: Angle = Angle()) -> None:
        GenericObject.__init__(self)
        self.weaponType = weaponType
        self.pos = pos
        self.angle = angle
        self.reloading = weaponType.rapidity
    
    def update(self) -> None:
        if self.reloading > 0:
            self.reloading -= 1
    
    def doesReach(self, other: Vector2d, location: int, mapSize: Vector2d, unitAngle: Angle) -> bool:
        if not self.weaponType.canAttack[location]:
            return False
        divercity = ((other - self.pos + (mapSize / 2)) % mapSize.x - (mapSize / 2))
        if not (-self.weaponType.distance <= divercity.x <= self.weaponType.distance and -self.weaponType.distance <= divercity.y <= self.weaponType.distance):
            return False
        if self.pos.distanceLooped(other, mapSize) > self.weaponType.distance:
            return False
        if self.weaponType.fov.angle == 2 * pi:
            return True
        if -self.weaponType.fov.angle / 2 <= (unitAngle.angle - (atan2(divercity.y, divercity.x) % (2 * pi)) + pi) % (2 * pi) - pi <= self.weaponType.fov.angle / 2:
            return True
        return False
    

class WeaponTypes:
    """
    Here might be all weapon types in the game
    """
    shipCanon = WeaponType("wal:weapon:ship_canon", Damage((380, 740, 960)), 11, 2, (0, 1, 1, 0, 0), 6, Angle(7 / 9 * 2 * pi))
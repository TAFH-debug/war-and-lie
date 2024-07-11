from server.vmath import *
from .generic import GenericObject, Damage

class WeaponType:
    id: int
    name: str
    damage: Damage
    rapidity: int # ticks between series
    shootSeries: int # how much shoots in series
    canAttack: tuple[bool]
    distance: float
    fov: Angle

    idCount = 0

    def __init__(self, name: str = "wal:weapon:none", damage: Damage = Damage((0, 0, 0)), rapidity: int = 0, shootSeries: int = 0, canAttack: tuple[bool] = (0, 0, 0, 0, 0), distance: float = 0, fov: Angle = Angle(0)) -> None:
        self.id = WeaponType.idCount
        WeaponType.idCount += 1
        self.name = name
        self.damage = damage
        self.rapidity = rapidity
        self.shootSeries = shootSeries
        self.canAttack = canAttack
        self.distance = distance
        self.fov = fov
    
    def as_bytes(self) -> bytes:
        return to_bytes(self.id)
        # all properties are accessable by id

    def __repr__(self) -> str:
        return f"Wtype = {self.name}"
    
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
        if not self.pos.fast_reach_test(other, mapSize, self.weaponType.distance):
            return False
        if self.weaponType.fov.angle == 2 * pi:
            return True
        if -self.weaponType.fov.angle / 2 <= (unitAngle.angle - (((other - self.pos + (mapSize / 2)) % mapSize.x - (mapSize / 2)).toAngle().angle % (2 * pi)) + pi) % (2 * pi) - pi <= self.weaponType.fov.angle / 2:
            return True
        return False
    
    def as_bytes(self) -> bytes:
        return merge(self.weaponType.as_bytes(), GenericObject.as_bytes(self))
    
    def __repr__(self) -> str:
        return f"WEAPON: <{self.weaponType}, {GenericObject.__repr__(self)}>"
    
class WeaponTypes:
    """
    Here might be all weapon types in the game
    """
    shipCanon = WeaponType("wal:weapon:ship_canon", Damage((380, 740, 960)), 27, 2, (0, 1, 1, 0, 0), 6, Angle(7 / 9 * 2 * pi))
    minerPickaxe = WeaponType("wal:weapon:minerPickaxe", Damage((700, 340, 670)), 32, 1, (0, 0, 1, 0, 0), 1.5, Angle(1 / 8 * 2 * pi))
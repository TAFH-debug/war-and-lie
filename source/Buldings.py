from .Map import Map
from .engine.vmath import *
from .generic import AliveInArmor, Damage, GenericAliveObject
from .textures import *
from .tile import Tile


class Buldings:
    texture: Texture
    size: Vector2d
    hp: AliveInArmor

    def __init__(self, texture: Texture, size: Vector2d, speed: float, hp: AliveInArmor) -> None:
        self.texture = texture
        self.size = size
        self.speed = speed
        self.hp = hp
        self.damage = damage

class Defender(Buldings): "Здания типа 'Защита' по типу башен и т.д."
    damage:Damage
    def __init__(self, damage: Damage):
        self.damage = damage;

class Industrial(Buldings): "Здания типа 'Производство' по типу завода и т.д."
    pass

class BuldingsTypes():
    """
    Here must be all Buldings types in the game
    """

class Building(GenericAliveObject):

    def __init__(self, buildingType: BuildingType, pos: Vector2d) -> None:
        super().__init__(buildingType.texture, buildingType.hp(), buildingType.hp.armorType, buildingType.hp.armor)
        self.pos = pos
        self.size = buildingType.size

    def upgrade(self):
        pass
    def repair(self):
        pass


class ConstructionSite:
    def __init__(self, buildingType: BuildingType, pos: Vector2d) -> None:
        self.building_type = buildingType
        self.pos = pos
        self.construction_progress = 0
        self.construction_speed = 1
        #Здесь можно добавить дополнительные свойства для механики строительства
    def construct(self):
        self.construction_progress += self.construction_speed
        if self.construction_progress >= 100:
            # Construction complete
            return Building(self.building_type, self.pos) #Если что замените, по нужде
        else:
            # Construction still in progress
            return None


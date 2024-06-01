from source.engine.vmath import Vector2d
from source.textures import Texture, Vector2d
from .engine.vmath import *
from .generic import AliveInArmor, Damage, GenericAliveObject
from .textures import Texture, Textures, TextureAsComponent
from .unit import UnitType, UnitTypes
from .resources import Cost, ResourceTypes

from source.engine.game_object import GameObject

class BuildingType:

    texture: Texture
    size: Vector2d
    hp: AliveInArmor
    cost: Cost
    constructionTime: int

    def __init__(self, texture: Texture, size: Vector2d, hp: AliveInArmor, cost: Cost, constructionTime: int) -> None:
        self.texture = texture
        self.size = size
        self.hp = hp
        self.cost = cost
        self.constructionTime = constructionTime

class Defender(BuildingType):
    damage: Damage

    def __init__(self, texture: Texture, size: Vector2d, hp: AliveInArmor, cost: Cost, constructionTime: int, damage: int) -> None:
        super().__init__(texture, size, hp, cost, constructionTime)
        self.damage = damage

class Industrial(BuildingType): 
    produces: tuple[UnitType]
    trainQueue: list[UnitType]

    def __init__(self, texture: Texture, size: Vector2d, hp: AliveInArmor, cost: Cost, constructionTime: int, produces: tuple[UnitType]) -> None:
        super().__init__(texture, size, hp, cost, constructionTime)
        self.produces = produces
        self.timer: int = 0
        self.trainQueue: list[UnitType] = []

    def addToQueue(self, unitType: UnitType) -> None:
        if unitType in self.produces:
            self.trainQueue.append(unitType)
        else:
            raise ValueError(f"{unitType} is not in {self.produces}")

    def removeFromQueue(self) -> None:
        if len(self.trainQueue) > 0:
            self.trainQueue.pop(-1)
        else:
            raise ValueError(f"produce queue is empty")

    def train(self) -> None:
        if len(self.trainQueue) == 0:
            raise ValueError("No units in queue to train")
        
        unitType = self.trainQueue[0]
        self.spawn_unit(unitType)

    def spawn_unit(self, unitType: UnitType) -> None:
        spawn_position = Vector2d(self.size.x + 1, self.size.y + 1)
        new_unit = unitType(spawn_position) 
        #тут должно быть добавления юнита в игру

    def iteration(self) -> None:
        if len(self.trainQueue) > 0:
            self.timer += 1
            if self.timer >= self.trainQueue[0].productionTime:
                self.train()
                self.trainQueue.pop(0)
                self.timer = 0


class BuldingsTypes():
    """
    Here have to be all buildings in the game
    """

    shipYard = Industrial(Textures.shipYard, Vector2d(3, 3), AliveInArmor(3, 10, 100), Cost({ResourceTypes.wood: 20}), 100, (UnitTypes.ship))

class Building(GenericAliveObject, GameObject):

    def __init__(self, buildingType: BuildingType, pos: Vector2d) -> None:
        GenericAliveObject.__init__(self, buildingType.texture, buildingType.hp.value, buildingType.hp.armorType, buildingType.hp.armor)
        self.pos = pos # position of upper-left corner
        self.size = buildingType.size

        GameObject.__init__(self, "Building")
        self.add_component(TextureAsComponent(self, buildingType.texture))
        self.transform.translate((pos + (self.size / 2)) * 64)


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

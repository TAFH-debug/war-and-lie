from .generic import AliveInArmor, GenericAliveObject
from .unit import UnitType, UnitTypes, Unit
from .resources import Cost, ResourceTypes
from .Map import Map
from .weapon import Weapon, WeaponType

from server.vmath import Vector2d, Direction, to_bytes, merge

class BuildingType:
    id: int
    name: str
    size: Vector2d
    hp: AliveInArmor
    cost: Cost
    body: tuple[Vector2d]
    constructionTime: int
    upgradesTo: "BuildingType"

    idCount = 0

    def __init__(self, name: str = "wal:building:none", size: Vector2d = Vector2d(1, 1), hp: AliveInArmor = AliveInArmor(0, 0, 0), cost: Cost = Cost({}), constructionTime: int = 0, body: tuple[Vector2d] = None, upgradesTo: "BuildingType" = None) -> None:
        self.id = BuildingType.idCount
        BuildingType.idCount += 1
        self.name = name
        self.size = size
        self.hp = hp
        self.cost = cost
        self.constructionTime = constructionTime
        self.body = body
        self.upgradesTo = upgradesTo

    def upgrade(self):
        BuildingType.__init__(
            self, 
            self.upgradesTo.name,
            self.upgradesTo.size, 
            self.upgradesTo.hp, 
            self.upgradesTo.cost,
            self.upgradesTo.constructionTime,
            self.upgradesTo.body,
            self.upgradesTo.upgradesTo
        )

    def as_bytes(self):
        return to_bytes(self.id)

    def __repr__(self) -> str:
        return f"Btype = {self.name}"

class Defender(BuildingType):
    weapons: tuple[WeaponType]

    def __init__(self, name: str, size: Vector2d, hp: AliveInArmor, cost: Cost, constructionTime: int, weapons: tuple[WeaponType], body: tuple[Vector2d] = None) -> None:
        super().__init__(name, size, hp, cost, constructionTime, body)
        self.weapons = weapons
    
    def as_bytes(self):
        return merge(BuildingType.as_bytes(self), self.weapons)

class Industrial(BuildingType): 
    produces: tuple[UnitType]

    def __init__(self, name: str, size: Vector2d, hp: AliveInArmor, cost: Cost, constructionTime: int, produces: tuple[UnitType], producePoint: Vector2d, body: tuple[Vector2d] = None) -> None:
        BuildingType.__init__(self, name, size, hp, cost, constructionTime, body)
        self.produces = produces
        self.producePoint = producePoint
    
    def upgrade(self):
        self.produces = self.upgradesTo.produces
        BuildingType.upgrade(self)

    def as_bytes(self):
            return merge(BuildingType.as_bytes(self), self.produces)
    

class BuildingTypes():
    """
    Here have to be all buildings in the game
    """

    shipYard = Industrial(
        "wal:building:ship_yard",
        Vector2d(3, 3),
        AliveInArmor(3, 10, 100),
        Cost({ResourceTypes.wood: 20}),
        100, 
        (UnitTypes.ship), 
        Vector2d(2, 1),
        (Vector2d(i%3, i//3) for i in (0, 1, 2, 3, 4, 6, 7, 8)))

class Building(GenericAliveObject):
    buildingType: BuildingType
    playerIndex: int
    direction: Direction

    def __init__(self, buildingType: BuildingType, playerIndex: int, pos: Vector2d, direction: Direction = Direction(0)) -> None:
        GenericAliveObject.__init__(self, buildingType.hp.value, buildingType.hp.armorType, buildingType.hp.armor)
        self.playerIndex = playerIndex
        self.pos = pos # position of upper-left corner
        self.size = buildingType.size
        self.buildingType = buildingType
        self.direction = direction
        self.buildingProgress = self.buildingType.constructionTime

    def placeOnMap(self, map: Map) -> None:
        if self.buildingType.body != None:
            center = (self.size - Vector2d(1, 1)) / 2
            if self.direction.value % 2 == 1:
                ncenter = Vector2d(center.y, center.x) 
            else:
                ncenter = Vector2d(center.x, center.y) 
            for vec in self.buildingType.body:
                map.get(self.direction.rotateVector2d(vec - center) + ncenter + self.pos).isTaken = True
        else:
            for y in range(self.size.y):
                for x in range(self.size.x):
                    map[y + self.pos.y][x + self.pos.x].isTaken = True

    def takeOfMap(self, map: Map) -> None:
        if self.buildingType.body != None:
            center = (self.size- Vector2d(1, 1)) / 2
            if self.direction.value % 2 == 1:
                ncenter = Vector2d(center.y, center.x) 
            else:
                ncenter = Vector2d(center.x, center.y) 
            for vec in self.buildingType.body:
                map.get(self.direction.rotateVector2d(vec - center) + ncenter + self.pos).isTaken = False
        else:
            for y in range(self.size.y):
                for x in range(self.size.x):
                    map[y + self.pos.y][x + self.pos.x].isTaken = False

    def upgrade(self) -> None:
        GenericAliveObject.__init__(self, self.buildingType.upgradesTo.hp.value, self.buildingType.upgradesTo.hp.armorType, self.buildingType.upgradesTo.hp.armor)
        self.buildingType.upgrade()
        self.buildingProgress = self.buildingType.constructionTime

    def repair(self):
        pass

    def update(self) -> bool:
        if self.buildingProgress != 0:
            self.buildingProgress -= 1
            return False
        return True

    def as_bytes(self):
        return merge(to_bytes(self.buildingType, self.playerIndex, self.direction), GenericAliveObject.as_bytes(self))

    def __repr__(self) -> str:
        return f"BUILDING: <{self.buildingType}, {GenericAliveObject.__repr__(self)}>"

class IndustrialBuilding(Building):
    def __init__(self, buildingType: Industrial, pos: Vector2d, direction: Direction = Direction(0)) -> None:
        Building.__init__(self, buildingType, pos, direction)
        self.producePoint = buildingType.producePoint
        self.trainQueue: list[UnitType] = []
        self.timer: int = 0
        center = (self.size - Vector2d(1, 1)) / 2
        if self.direction.value % 2 == 1:
            ncenter = Vector2d(center.y, center.x) 
        else:
            ncenter = Vector2d(center.x, center.y) 
        self.producePoint = (self.direction.rotateVector2d(self.producePoint - center) + ncenter)

    def addToQueue(self, unitType: UnitType) -> None:
        if unitType in self.buildingType.produces:
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

    def update(self) -> bool:
        if not Building.update(self):
            return False
        if len(self.trainQueue) > 0:
            self.timer += 1
            if self.timer >= self.trainQueue[0].productionTime:
                self.train()
                self.trainQueue.pop(0)
                self.timer = 0
        return True

    def spawn_unit(self, unitType: UnitType, map: Map) -> None:
        u = Unit(unitType, self.playerIndex, self.producePoint + self.pos, self.direction.toAngle())
        u.placeOnMap(map)
    
    def as_bytes(self):
        return merge(Building.as_bytes(self), to_bytes(self.trainQueue, self.timer))

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

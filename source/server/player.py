from .unit import Unit
from .building import Building, BuildingTypes, IndustrialBuilding
from .resources import Resource, ResourceTypes
from .Map import Map, Landscapes
from .technology import Tech

from server.vmath import Vector2d, to_bytes

class Player:
    id: int
    name: str
    units: list[Unit]
    buildings: list[Building]
    resources: list[Resource]
    vision: list[list[bool]]
    visible: list[Unit|Building]
    techs: list[Tech]

    idCount = 0

    def __init__(self, name: str = "player") -> None:
        self.id = Player.idCount
        Player.idCount += 1
        self.name = name

    def setName(self, name: str) -> None:
        self.name = name

    def initSpectator(self, world: Map) -> None:
        self.units = [] 
        self.buildings = []
        self.techs = []
        self.visible = []
        self.resources = [Resource(rType, 0, 0) for rType in ResourceTypes.allResources]
        self.vision = [[True for _ in world] for _ in world[0]]
        self.vision_updates = [[True for _ in world] for _ in world[0]]

    def initTest(self, world: Map) -> None:
        self.units = [] 
        self.buildings = [IndustrialBuilding(BuildingTypes.shipYard, self.id, Vector2d(self.id * 5 + 3, self.id * 5 + 3))]
        self.techs = []
        self.visible = []
        self.resources = [Resource(rType, 0, 0) for rType in ResourceTypes.allResources]
        self.vision = [[False for _ in world] for _ in world[0]]
        self.vision_updates = [[False for _ in world] for _ in world[0]]
    
    # returns whether units vision had changed
    def updateVision(self, world: Map) -> bool:
        self.vision_updates = [[False for _ in world] for _ in world[0]]
        needUpdate = False
        for unit in self.units:
            for y in range(len(self.vision)):
                for x in range(len(self.vision[y])):
                    if self.vision[y][x]:
                        if not unit.pos.fast_reach_test(Vector2d(x, y), world.size, unit.unitType.visionRange):
                            self.vision[y][x] = False
                            needUpdate = True
                    elif unit.pos.fast_reach_test(Vector2d(x, y), world.size, unit.unitType.visionRange):
                        needUpdate = True
                        self.vision[y][x] = True
                        self.vision_updates[y][x] = True
        return needUpdate

    def iteration(self, world: Map) -> bool:
        """
        Updates all game events
        Returns whether player need update in information
        """
        if len(self.units) == 0 and len(self.buildings) == 0:
            return False
        needUpdate = False
        needVisionUpdate = False
        for unit in self.units:
            res = unit.update(world)
            needUpdate |= res[0]
            needVisionUpdate |= res[1]
        for building in self.buildings:
            res = building.update(world, self.units)
            needUpdate |= res[0]
            needVisionUpdate |= res[1]
        if needVisionUpdate:
            needUpdate |= self.updateVision(world)
        for obj in self.visible:
            if obj.needUpdate:
                needUpdate = True
                break
        return needUpdate

    def __repr__(self) -> str:
        return f"PLAYER: <<{self.name}>, buildings: <{self.buildings}>, units: <{self.units}>, resources: <{self.resources}>>"

class Game:
    name: str
    players: list[Player]
    world: Map

    def __init__(self, name:str, playerNumber: int, mapSize: Vector2d) -> None:
        self.name = name
        self.world = Map(mapSize)
        self.players = [Player(i) for i in range(playerNumber)]

    def initVoid(self) -> None:
        self.world.initEmpty()
        for player in self.players:
            player.initSpectator(self.world)
    
    def initTest(self) -> None:
        self.world.initEmpty()
        for player in self.players:
            player.initTest(self.world)
    
    def getPlayersData(self, playerIndex: int) -> bytearray:
        result = []
        vis = []
        units = []
        buildings = []
        for y in range(self.world.size.y):
            for x in range(self.world.size.x):
                if self.players[playerIndex].vision_updates[y][x]:
                    vis.append(self.world[y][x])
                if self.players[playerIndex].vision[y][x]:
                    for player in self.players:
                        if player == self.players[playerIndex]:
                            continue
                        for unit in player.units:
                            if Vector2d(x, y).isInBox(unit.pos, unit.pos + unit.size):
                                units.append(unit)
                        for building in player.buildings:
                            if Vector2d(x, y).isInBox(building.pos, building.pos + building.size):
                                buildings.append(building)
        self.players[playerIndex].visible.clear()
        self.players[playerIndex].visible.extend(units)
        self.players[playerIndex].visible.extend(buildings)
        units.extend(self.players[playerIndex].units)
        buildings.extend(self.players[playerIndex].buildings)
        result.append(vis)
        result.append(buildings)
        result.append(units)
        return to_bytes(result)

    def iteration(self) -> int:
        needUpdatesFor = 0
        for i in range(len(self.players)):
            needUpdate = self.players[i].iteration(self.world)
            needUpdatesFor += int(needUpdate) * (2 ** i)
        return needUpdatesFor

    def __repr__(self) -> str:
        return f"GAME: <{self.players}>"

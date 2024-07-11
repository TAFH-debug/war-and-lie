from .unit import Unit
from .building import Building
from .resources import Resource, ResourceTypes
from .Map import Map
from .technology import Tech

from server.vmath import Vector2d, to_bytes

class Player:
    id: int
    name: str
    units: list[Unit]
    buildings: list[Building]
    resources: list[Resource]
    vision: list[list[bool]]
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
        self.resources = [Resource(rType, 0, 0) for rType in ResourceTypes.allResources]
        self.vision = [[True for _ in world] for _ in world[0]]
        self.vision_updates = [[True for _ in world] for _ in world[0]]

    def updateVision(self, world: Map):
        self.vision_updates = [[False for _ in world] for _ in world[0]]
        for unit in self.units:
            for y in range(len(self.vision)):
                for x in range(len(self.vision[y])):
                    if self.vision[y][x]:
                        if not unit.pos.fast_reach_test(Vector2d(x, y), world.size, unit.unitType.visionRange):
                            self.vision[y][x] = False
                            self.vision_updates[y][x] = True
                    elif unit.pos.fast_reach_test(Vector2d(x, y), world.size, unit.unitType.visionRange):
                        self.vision[y][x] = True
                        self.vision_updates[y][x] = True
    
    def __repr__(self) -> str:
        return f"PLAYER: <{self.name}>, buildings: <" + str(self.buildings) + ">, units: <" + str(self.units) + ">, resources: <" + str(self.resources) + ">>"

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
    
    def getPlayersData(self, playerIndex: int) -> bytearray:
        result = []
        vis = []
        for y in range(self.world.size.y):
            for x in range(self.world.size.x):
                if self.players[playerIndex].vision_updates[y][x]:
                    vis.append(self.world[y][x])
        result.append(vis)
        result.append(self.players[playerIndex].buildings)
        result.append(self.players[playerIndex].units)
        return to_bytes(result)
    
    def __repr__(self) -> str:
        return f"GAME: <{self.players}>"

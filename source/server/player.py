from .unit import Unit
from .bulding import Building
from .resources import Resource, ResourceTypes
from .Map import Map

from source.engine.vmath import Vector2d

class Player:
    index: int
    name: str
    units: list[Unit]
    buildings: list[Building]
    resources: list[Resource]
    vision: list[list[bool]]

    def __init__(self, index: int = 0, name: str = "player") -> None:
        self.index = index
        self.name = name

    def setName(self, name: str) -> None:
        self.name = name

    def initSpectator(self, world: Map) -> None:
        self.units = []
        self.buildings = []
        self.resources = [Resource(rType, 0, 0) for rType in ResourceTypes.allResources]
        self.vision = [[True for _ in world] for _ in world[0]]

class Game:
    name: str
    players: list[Player]
    world: Map

    def __init__(self, name:str, playerNumber: int, mapSize: Vector2d) -> None:
        self.name = name
        self.world = Map(mapSize)
        self.players = [Player(i) for i in range(playerNumber)]

    def initVoid(self) -> None:
        self.map.initEmpty()
        for player in self.players:
            player.initSpectator(self.world)
    
    def getPlayersData(self, playerIndex: int) -> bytearray:
        # TODO have to pack all data to send player 
        pass 

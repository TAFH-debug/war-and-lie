from .Map import Map
from .engine.vmath import *
from .generic import AliveInArmor, Damage, GenericAliveObject
from .textures import *
from .tile import Tile
from .resources import Cost, ResourceTypes


class UnitType:
    texture: Texture
    size: Vector2d
    speed: float
    hp: AliveInArmor
    damage: Damage
    cost: Cost
    productionTime: int

    def __init__(self, texture: Texture, size: Vector2d, speed: float, hp: AliveInArmor, damage: Damage, cost: Cost, productionTime: int) -> None:
        self.texture = texture
        self.size = size
        self.speed = speed
        self.hp = hp
        self.damage = damage
        self.cost = cost
        self.productionTime = productionTime


class UnitTypes():
    """
    Here must be all unit types in the game
    """

    ship = UnitType(Textures.ship, Vector2d(2, 2), 20, AliveInArmor(2, 10, 100), Damage((10, 23, 20)), Cost({ResourceTypes.wood: 3}), 10)


class Unit(GenericAliveObject):
    speed: float
    damage: Damage

    def __init__(self, unitType: UnitType, pos: Vector2d, direction: Angle) -> None:
        super().__init__(unitType.texture, unitType.hp(), unitType.hp.armorType, unitType.hp.armor)
        self.pos = pos
        self.direction = direction
        self.speed = unitType.speed
        self.damage = unitType.damage
        self.size = unitType.size
        self.path: list[Tile] = []
        self.current = 0
        # TODO tile where unit stands have to be indicated as taken

    def pathFinding(self, map: Map, endPoint: Tile) -> list[Tile]:  # A* algorithm
        # да здравствует лапша-код!
        # талим, будет время перепеши нормальный алгоритм поиска пути
        # TODO for talim and bfs for path finding.
        opened: list[tuple[Tile, float, float, int]] = []
        closed: list[tuple[Tile, float, float, int]] = []

        def isIn(pos: Vector2d, smth: list[tuple[Tile, float, float, int]]) -> tuple[
            bool, tuple[Tile, float, float, int] | None]:
            for l in smth:
                if l[0].pos == pos:
                    return (True, l)
            return (False, None)

        opened.append((map.get(Vector2d(int(self.pos.x), int(self.pos.y))), 0, 0, -1))
        while True:
            Min = opened[0][1] + opened[0][2]
            currInd = 0
            for i in range(len(opened)):
                if opened[i][1] + opened[i][2] < Min:
                    currInd = i
                    Min = opened[i][1] + opened[i][2]
            current = opened[currInd]
            # print(current[0].pos, current[1], current[2])
            opened.remove(current)
            closed.append(current)
            if current[0] == endPoint:
                break
            for relate in current[0].getRelatedCords(map.size):
                if map.get(Vector2d(int(relate.x), int(relate.y))).isTaken or isIn(relate, closed)[0]:
                    continue
                b, l = isIn(relate, opened)
                assert type(l) == tuple[Tile, float, float, int]
                newG = current[1] + current[0].pos.distanceLooped(relate, map.size) * map.get(
                    Vector2d(int(relate.x), int(relate.y))).landscape.passability
                if not b:
                    opened.append((map.get(Vector2d(int(relate.x), int(relate.y))), newG,
                                   endPoint.pos.distanceLooped(relate, map.size), len(closed) - 1))
                elif l[1] > newG:
                    opened[opened.index(l)] = (l[0], newG, l[2], len(closed) - 1)
        self.path = []
        current = closed[-1]
        while True:
            self.path.append(current[0])
            if current == closed[0]:
                break
            current = closed[current[3]]
        return self.path

    def rotate(self, angularVelocity: float):
        pass

    def move(self):  #
        pass

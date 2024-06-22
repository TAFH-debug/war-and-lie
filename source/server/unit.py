from .Map import Map
from  server.vmath import *
from .generic import AliveInArmor, Damage, GenericAliveObject
from .tile import Tile, Landscapes
from .resources import Cost, ResourceTypes
from .weapon import Weapon, WeaponTypes

# from source.engine.game_object import GameObject

class UnitLocatingTypes:
    UNDER_WATER = 0
    ON_WATER = 1
    ON_GROUND = 2
    ABOVE_GROUND = 3
    IN_AIR = 4


class UnitType:
    id: str
    size: Vector2d
    speed: float # tile per 20 ticks
    angularSpeed: Angle # per 20 ticks
    locations: tuple[bool]
    hp: AliveInArmor
    weapons: tuple[Weapon]
    cost: Cost
    productionTime: int

    def __init__(self, id: str = "wal:unit:none", size: Vector2d = Vector2d(1, 1), speed: float = 0, angularSpeed: Angle = Angle(0), locations: tuple[int] = (), hp: AliveInArmor = AliveInArmor(1, 0, 0), weapons: tuple[Weapon] = (), cost: Cost = Cost({}), productionTime: int = 0) -> None:
        self.id = id
        self.size = size
        self.speed = speed
        self.angularSpeed = angularSpeed
        self.locations = (i in locations for i in range(5))
        self.hp = hp
        self.weapons = weapons
        self.cost = cost
        self.productionTime = productionTime
    

class UnitTypes():
    """
    Here must be all unit types in the game
    """

    ship = UnitType("wal:unit:ship", Vector2d(2, 2), 0.76, Angle(1 / 9 * pi), (UnitLocatingTypes.ON_WATER,), AliveInArmor(3, 30, 6000), (WeaponTypes.shipCanon,), Cost({ResourceTypes.wood: 3}), 1000)
    miner = UnitType("wal:unit:miner", Vector2d(1, 1), 1.2, Angle(1 / 4 * pi), (UnitLocatingTypes.ON_GROUND,), AliveInArmor(1, 4, 1300), (WeaponTypes.minerPickaxe,), Cost({ResourceTypes.wood: 1}), 320)

class Unit(GenericAliveObject):
    unitType: UnitType
    playerIndex: int
    speed: float
    movementProgress: float
    angularSpeed: Angle
    weapons: tuple[Weapon]

    def __init__(self, unitType: UnitType, playerIndex: int, pos: Vector2d = Vector2d(0, 0), angle: Angle = Angle(0)) -> None:
        GenericAliveObject.__init__(self, unitType.hp.value, unitType.hp.armorType, unitType.hp.armor)
        self.unitType = unitType
        self.playerIndex = playerIndex
        self.pos = pos
        self.angle = angle
        self.speed = unitType.speed
        self.angularSpeed = unitType.angularSpeed
        self.weapons = tuple(Weapon(wType, pos, angle) for wType in unitType.weapons)
        self.size = unitType.size
        self.path: list[Tile] = []

    def pathFinding(self, map: Map, endPoint: Tile) -> list[Tile]:  # A* algorithm
        # да здравствует лапша-код!
        # талим, будет время перепеши нормальный алгоритм поиска пути
        # TODO for talim and bfs for path finding.
        opened: list[tuple[Tile, float, float, int]] = []
        closed: list[tuple[Tile, float, float, int]] = []

        def isIn(pos: Vector2d, smth: list[tuple[Tile, float, float, int]]) -> tuple[bool, tuple[Tile, float, float, int] | None]:
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
                if isIn(relate, closed)[0] or map.get(Vector2d(int(relate.x), int(relate.y))).isTaken:
                    continue
                # if not map.get(Vector2d(int(relate.x), int(relate.y))).landscape == Landscapes.water:
                #     continue # TODO this shit have to be checked another way
                b, l = isIn(relate, opened)
                newG = current[1] + current[0].pos.distanceLooped(relate, map.size) * map.get(
                    Vector2d(int(relate.x), int(relate.y))).landscape.passability
                if not b:
                    opened.append((map.get(Vector2d(int(relate.x), int(relate.y))), newG,
                                   endPoint.pos.distanceLooped(relate, map.size), len(closed) - 1))
                elif l[1] > newG:
                    assert type(l) == tuple and type(l[0]) == Tile and type(l[1]) == type(l[2]) == float and type(l[3]) == int
                    opened[opened.index(l)] = (l[0], newG, l[2], len(closed) - 1)
        self.path = []
        current = closed[-1]
        while True:
            self.path.append(current[0])
            if current == closed[0]:
                break
            current = closed[current[3]]
        self.path.reverse()
        self.path.pop(0)
        return self.path

    def placeOnMap(self, map: Map):
        map.get(self.pos).isTaken = True

    def takeOfMap(self, map: Map):
        map.get(self.pos).isTaken = False

    def setPos(self, pos: Vector2d, map: Map):
        self.takeOfMap(map)
        self.pos = pos
        for weapon in self.weapons:
            weapon.pos = pos
        self.placeOnMap(map)

    def rotate(self) -> bool:
        needed = (self.path[0].pos - self.pos).toAngle()
        deviation = self.angle - needed
        if round(deviation.angle, 6) == 0:
            return True
        self.movementProgress = 0
        if deviation.angle > pi:
            if 2*pi - deviation.angle < (self.angularSpeed.angle / 20):
                self.angle = needed
                return False
            self.angle = self.angle + Angle(self.angularSpeed.angle / 20)
            return False
        else:
            if deviation.angle < (self.angularSpeed.angle / 20):
                self.angle = needed
                return False
            self.angle = self.angle - Angle(self.angularSpeed.angle / 20)
            return False

    def move(self, map: Map):  #
        self.movementProgress += self.speed / 20
        if self.movementProgress >= self.path[0].pos.distanceLooped(self.pos, map.size):
            self.movementProgress -= self.path[0].pos.distanceLooped(self.pos, map.size)
            self.setPos(self.path[0].pos, map)
            self.path.pop(0)

    def update(self, map: Map):
        if len(self.path) != 0:
            isEnough = self.rotate()
            if isEnough:
                self.move(map)

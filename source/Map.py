from generic import GenericMap
from tile import *


class Map(GenericMap[Tile]):
    def __init__(self, size: Vector2d) -> None:
        super().__init__(size)

    def initEmpty(self) -> None:
        self.Map = [[Tile(Vector2d(x, y), Landscapes.water) for x in range(self.size.intx())] for y in
                    range(self.size.inty())]

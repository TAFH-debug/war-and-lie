from source.util import DoubleNumber
from .generic import GenericMap
from .tile import *

class Map(GenericMap[Tile]):
    def __init__(self, size: DoubleNumber[int]) -> None:
        super().__init__(size)

    def initEmpty(self) -> None:
        self.Map = [[Tile(DoubleNumber(x, y), Landscapes.water) for x in range(self.size.x)] for y in range(self.size.y)]

from .generic import GenericMap
from .tile import Tile, Landscapes

from source.vmath import Vector2d

class Map(GenericMap[Tile]):
    def __init__(self, size: Vector2d) -> None:
        GenericMap.__init__(self, size)

    def initEmpty(self) -> None:
        self.Map = [[
            Tile(Vector2d(x, y), Landscapes.water) 
            for x in range(self.size.intx())] 
            for y in range(self.size.inty())]
    
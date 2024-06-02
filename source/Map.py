from pygame import Surface
from .generic import GenericMap
from .tile import Tile, Landscapes

from source.engine.game_object import GameObject
from source.engine.vmath import Vector2d

class Map(GenericMap[Tile], GameObject):
    def __init__(self, size: Vector2d) -> None:
        GenericMap.__init__(self, size)
        GameObject.__init__(self, "Map")

    def initEmpty(self) -> None:
        self.Map = [[
            Tile(Vector2d(x, y), Landscapes.water) 
            for x in range(self.size.intx())] 
            for y in range(self.size.inty())]
    
    def draw(self, display: Surface) -> None:
        for x in range(self.size.intx()):
            for y in range(self.size.inty()):
                self.Map[y][x].draw(display)

    
from .generic import GenericObject
from .util import DoubleNumber
from .textures import *

class Landscape:
    # TODO some other parameters are required
    passability: int # multiply the time needed for unit to pass this tile by passability
    texture: Texture

    def __init__(self, passability: int, texture: Texture) -> None:
        self.passability = passability
        self.texture = texture

class Landscapes():
    """
    Here shall be all landscape types in the game
    """
    # example landscape
    water = Landscape(2, Textures.water)

class Tile(GenericObject):
    landscape: Landscape
    height: int # TODO in another version height have to be used
    isTaken: bool # if smth\smbd stands on this tile

    def __init__(self, pos: DoubleNumber[int, int], landscape: Landscape) -> None:
        GenericObject().__init__(landscape.texture)
        self.pos = pos
        self.landscape = landscape
        self.isTaken = False
        

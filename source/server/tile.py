from .generic import GenericObject

from source.vmath import Vector2d

class Landscape:
    # TODO some other parameters are required
    passability: int  # multiply the time needed for unit to pass this tile by passability
    id: str

    def __init__(self, id: str, passability: int) -> None:
        self.passability = passability
        self.id = id


class Landscapes():
    """
    Here shall be all landscape types in the game
    """
    # example landscape
    water = Landscape("wal:tile:water", 2)


class Tile(GenericObject):
    landscape: Landscape
    height: int  # TODO in another version height have to be used
    isTaken: bool  # if smth\smbd stands on this tile

    def __init__(self, pos: Vector2d, landscape: Landscape) -> None:

        GenericObject.__init__(self)
        self.pos = pos
        self.landscape = landscape
        self.isTaken = False

    def __eq__(self, other: "Tile") -> bool:
        return (self.pos == other.pos)

    def __ne__(self, other: "Tile") -> bool:
        return (self.pos != other.pos)

from .generic import GenericObject

from server.vmath import Vector2d, to_bytes

class Landscape:
    # TODO some other parameters are required
    passability: int  # multiply the time needed for unit to pass this tile by passability
    name: str
    id: int

    idCount = 0

    def __init__(self, name: str, passability: int) -> None:
        self.id = Landscape.idCount
        Landscape.idCount += 1
        self.name = name
        self.passability = passability
    
    def __eq__(self, other: "Landscape") -> bool:
        return self.id == other.id 

    def as_bytes(self) -> bytes:
        return to_bytes(bytes((self.id, )))

class Landscapes():
    """
    Here shall be all landscape types in the game
    """
    # example landscape
    water = Landscape("wal:tile:water", 2)


class Tile(GenericObject):
    landscape: Landscape
    height: int = 0 # TODO in another version height have to be used
    isTaken: bool  # if smth\smbd stands on this tile

    def __init__(self, pos: Vector2d, landscape: Landscape) -> None:

        GenericObject.__init__(self)
        self.pos = pos
        self.landscape = landscape
        self.isTaken = False

    def as_bytes(self) -> bytes:
        return to_bytes((self.landscape, self.pos, self.height))

    def __eq__(self, other: "Tile") -> bool:
        return (self.pos == other.pos)

    def __ne__(self, other: "Tile") -> bool:
        return (self.pos != other.pos)

    def __repr__(self) -> str:
        return f"TILE: <{self.landscape}, {self.pos}"
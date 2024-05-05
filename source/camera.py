from .util import *


class __Camera:
    x: int
    y: int
    zoom: float
    
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.zoom = 0
    
    def normalize(self, pos: DoubleNumber) -> DoubleNumber:
        """
        Normalizes pos coordinates to relative to camera coordinates.
        """
        
        # TODO: Zoom in/out
        return DoubleNumber(pos.x - self.x, pos.y - self.y)


"""
A lot of boilerplate code.
Needed for comfortability and peace of mind.
"""
__camera = __Camera()

def normalize(pos: DoubleNumber | tuple[int, int]) -> DoubleNumber:
    if isinstance(pos, tuple):
        return __camera.normalize(DoubleNumber.from_tuple(pos))
    return __camera.normalize(pos)

def set_x(x: int):
    __camera.x = x
    
def set_y(y: int):
    __camera.y = y
    
def set_position(pos: DoubleNumber | tuple[int, int]):
    if isinstance(pos, tuple):
        pos = DoubleNumber.from_tuple(pos)
    __camera.x = pos.x
    __camera.y = pos.y
    
def change_x(x: int):
    __camera.x += x
    
def change_y(y: int):
    __camera.y += y
    
def change_pos(pos: DoubleNumber | tuple[int, int]):
    if isinstance(pos, tuple):
        pos = DoubleNumber.from_tuple(pos)
    __camera.x += pos.x
    __camera.y += pos.y
    
def get_x():
    return __camera.x

def get_y():
    return __camera.y

def get_pos():
    return DoubleNumber(__camera.x, __camera.y)


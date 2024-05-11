from .vmath import *


class Camera:
    x: int
    y: int
    zoom: float
    
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.zoom = 0
    
    def normalize_helper(self, pos: DoubleNumber) -> DoubleNumber:
        """
        Normalizes pos coordinates to relative to camera coordinates.
        """
        
        # TODO: Zoom in/out
        return DoubleNumber(pos.x - self.x, pos.y - self.y)
    
    def normalize(self, pos: DoubleNumber | tuple[int, int]) -> DoubleNumber:
        if isinstance(pos, tuple):
            return self.normalize_helper(DoubleNumber.from_tuple(pos))
        return self.normalize_helper(pos)
    
    def set_x(self, x: int):
        self.x = x
        
    def set_y(self, y: int):
        self.y = y
        
    def set_position(self, pos: DoubleNumber | tuple[int, int]):
        if isinstance(pos, tuple):
            pos = DoubleNumber.from_tuple(pos)
        self.x = pos.x
        self.y = pos.y
        
    def change_x(self, x: int):
        self.x += x
        
    def change_y(self, y: int):
        self.y += y
        
    def change_pos(self, pos: DoubleNumber | tuple[int, int]):
        if isinstance(pos, tuple):
            pos = DoubleNumber.from_tuple(pos)
        self.x += pos.x
        self.y += pos.y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_pos(self):
        return DoubleNumber(self.x, self.y)

camera = Camera()

import pygame
from pygame import Surface
from source.engine.util import DoubleNumber

SPRITE_PATH = "./sprites"

class Texture:
    
    def __init__(self, surface: Surface, size: DoubleNumber[int], frames: int = 1, fullAnimTimeInTicks: int = 25):
        self.surface: Surface = surface
        self.frames: int = frames
        self.current: int = 0
        self.width, self.height = size.x, size.y
        self.fullAnimTime: int = fullAnimTimeInTicks
        
        
class Textures():
    """
    There should be all textures that will be used in game.
    For optimisation purposes.
    """
    
    
    # Example texture
    ship = Texture(pygame.image.load(SPRITE_PATH + "/ship.png"), DoubleNumber(64, 64), 4)
    water = Texture(pygame.image.load(SPRITE_PATH + "/water.png"), DoubleNumber(64, 64), 1)
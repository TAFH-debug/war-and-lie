import pygame
from pygame import Surface

SPRITE_PATH = "./sprites"

class Texture:
    
    def __init__(self, surface: Surface, size: tuple[int, int], frames: int = 1):
        self.surface: Surface = surface
        self.frames: int = frames
        self.current: int = 0
        self.width, self.height = size
        
        
class Textures():
    """
    There should be all textures that will be used in game.
    For optimisation purposes.
    """
    
    
    # Example texture
    ship = Texture(pygame.image.load(SPRITE_PATH + "/ship.png"), (64, 64), 2)
    water = Texture(pygame.image.load(SPRITE_PATH + "/water.png"), (64, 64), 1)
import pygame
from pygame import Surface

from source.engine.vmath import Vector2d
from source.engine.game_object import Component, GameObject

SPRITE_PATH = "./sprites"


class Texture:

    def __init__(self, surface: Surface, size: Vector2d, frames: int = 1, fullAnimTimeInTicks: int = 25):
        self.surface: Surface = surface
        self.frames: int = frames
        self.current: int = 0
        self.size = size
        self.fullAnimTime: int = fullAnimTimeInTicks


# General class for all textures
class HasTexture:

    def __init__(self, texture: Texture):
        self.texture: Texture = texture
        self.surface: Surface = texture.surface
        self.frames: int = texture.frames
        self.current: int = 0
        self.fullAnimTime: int = texture.fullAnimTime
        self.AnimTimer: int = 0
        self.textureSize = Vector2d(texture.width, texture.height)

    # Counts frames and borders them by variable "frames"
    def nextFrame(self) -> None:
        self.current = (self.current + 1) % self.frames

    # gives current frame's positions and size
    def getFrameCoords(self, curr: int | None = None) -> tuple[int, int, int, int]:
        if curr == None:
            curr = self.current
        return ((self.textureSize.intx() * self.current), 0, self.textureSize.intx(), self.textureSize.inty())

    def iteration(self) -> None:
        self.AnimTimer += 1
        if self.AnimTimer == self.fullAnimTime:
            self.AnimTimer = 0
            self.nextFrame()

class TextureAsComponent(Component):

    def __init__(self, obj: GameObject, texture: Texture):
        Component.__init__(self, obj)
        self.texture = texture
    
    def draw(self, display: Surface):
        display.blit(self.texture.surface, (self.game_object.transform.position - (self.texture.size / 2)).as_tuple())

class Textures():
    """
    There should be all textures that will be used in game.
    For optimisation purposes.
    """

    # Example texture
    ship = Texture(pygame.image.load(SPRITE_PATH + "/ship.png"), Vector2d(64, 64), 4)
    water = Texture(pygame.image.load(SPRITE_PATH + "/water.png"), Vector2d(64, 64), 1)
#    shipYard = Texture(pygame.image.load(SPRITE_PATH + "/shipYard.png"), Vector2d(64, 64), 1)

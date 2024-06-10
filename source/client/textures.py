import pygame
from pygame import Surface
from math import cos, sin, pi

from engine.vmath import Vector2d, Angle
from engine.game_object import Component, GameObject

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
        self.textureSize: Vector2d = texture.size

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
    
    def blit(self, display: Surface, cords: Vector2d, angle: Angle = Angle(0), scale: float = 1) -> None:
        blitImage = Surface((self.textureSize.x, self.textureSize.y), pygame.SRCALPHA, 32)
        blitImage = blitImage.convert_alpha()
        blitImage.blit(self.surface, (0, 0), self.getFrameCoords())
        nx = cords.x
        ny = cords.y
        if angle.get() != 0:
            blitImage = pygame.transform.rotate(blitImage, angle.get(True))
            nx -= int(self.textureSize.x * (cos(angle.get() % (pi / 2)) + sin(angle.get() % (pi / 2)) - 1) / 2)
            ny -= int(self.textureSize.y * (cos(angle.get() % (pi / 2)) + sin(angle.get() % (pi / 2)) - 1) / 2)
        if scale != 1:
            blitImage = pygame.transform.scale_by(blitImage, scale)
            nx //= scale
            ny //= scale
        display.blit(blitImage, (nx, ny))

class TextureAsComponent(Component, HasTexture):

    def __init__(self, obj: GameObject, texture: Texture):
        Component.__init__(self, obj)
        HasTexture.__init__(self, texture)
    
    def draw(self, display: Surface):
        self.blit(
            display, 
            (self.game_object.transform.position - (self.texture.size / 2)), 
            self.game_object.transform.angle
        )

class Textures():
    """
    There should be all textures that will be used in game.
    For optimisation purposes.
    """

    # Example texture
    ship = Texture(pygame.image.load(SPRITE_PATH + "/ship.png"), Vector2d(64, 64), 4)
    water = Texture(pygame.image.load(SPRITE_PATH + "/water.png"), Vector2d(64, 64), 1)
    shipYard = Texture(pygame.image.load(SPRITE_PATH + "/shipYard.png"), Vector2d(192, 192), 1)

from pygame import Surface
import pygame
from .textures import Texture
from .engine.vmath import *
from typing import Iterable
from math import cos, sin

# Needed for hp (or other things that have max value and are positive only)
class Alive:
    
    def __init__(self, maxValue: int, value: int | None = None):
        self.value: int = value or maxValue
        self.maxValue: int = maxValue
        
    # increase value and border it by max value
    def regenerate(self, value: int) -> None:
        self.value = min(self.value + value, self.maxValue)
        
    # decreases value and checks if it is positive
    def gainDamage(self, value: int) -> bool:
        self.value -= value
        return self.isAlive()
    
    # checks if it is positive
    def isAlive(self) -> bool:
        return self.value > 0
    
    # makes it easy to access to value (use " a() ")
    def __call__(self) -> int:
        return self.value

class Damage:
    damage: list[int]

    def __init__(self, damage: Iterable[int]) -> None:
        self.damage = list(damage)

    def __getitem__(self, index: int) -> int:
        return self.damage[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.damage[index] = value

class AliveInArmor(Alive):
    armorType: int
    armor: int

    def __init__(self, armorType: int, armor: int, maxValue: int, value: int | None = None) -> None:
        super().__init__(maxValue, value)
        self.armorType = armorType
        self.armor = armor

    def gainDamage(self, damage: Damage) -> bool:
        return super().gainDamage(damage[self.armorType] * (100 - self.armor) // 100)


# for money, resources and so on
class CountAble: 
    def __init__(self, value: int, income: int):
        self.value = value
        self.income = income
    # changes value. change can be negative also
    def change(self, value: int | None = None): 
        if value == None: 
            self.value += self.income
        else:
            self.value = value

# General class for all textures
class HasTexture: 
    
    def __init__(self, texture: Texture):
        self.texture: Texture = texture
        self.surface: Surface = texture.surface
        self.frames: int = texture.frames
        self.current: int = 0
        self.fullAnimTime: int = texture.fullAnimTime
        self.AnimTimer: int = 0
        self.textureSize = DoubleNumber(texture.width, texture.height)
        
    # Counts frames and borders them by variable "frames"
    def nextFrame(self) -> None: 
        self.current = (self.current + 1) % self.frames
        
    # gives current frame's positions and size
    def getFrameCoords(self, curr: int | None = None) -> tuple[int, int, int, int]:
        if curr == None:
            curr = self.current 
        return (self.textureSize.x * self.current, 0, self.textureSize.x, self.textureSize.y)
    
    def iteration(self) -> None:
        self.AnimTimer += 1
        if self.AnimTimer == self.fullAnimTime:
            self.AnimTimer = 0
            self.nextFrame()

    # blits texture on display
    # TODO texture also should be able to rotated and scaled
    def blit(self, display: Surface, cords: DoubleNumber, angle: Angle = Angle(0), scale: float = 1) -> None: 
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

# generic class for all objects that has texture and position
class GenericObject(HasTexture):
    pos: Vector2d
    size: DoubleNumber
    direction: Angle
    
    def __init__(self, texture: Texture) -> None:
        super().__init__(texture)
    
    def getRelatedCords(self, size: Vector2d) -> list[Vector2d]:
        delta = [
            Vector2d(-1, -1),
            Vector2d(0, -1),
            Vector2d(1, -1),
            Vector2d(1, 0),
            Vector2d(1, 1),
            Vector2d(0, 1),
            Vector2d(-1, 1),
            Vector2d(-1, 0)
        ]
        result = []
        for d in range(8):
            # TODO it should be voted for cycled or bordered map
            result.append((self.pos + delta[d]).operation(size, lambda a, b: a % b)) 
        return result
    def update(self, events: list[pygame.event.Event]):
        pass
    
    def draw(self, window: Surface): 
        pass

class GenericAliveObject(GenericObject, AliveInArmor):
    
    velocity: Vector2d

    def __init__(self, texture: Texture, hp: int, armorType: int, armor: int) -> None:
        GenericObject.__init__(self, texture) 
        AliveInArmor.__init__(self, armorType, armor, hp) 
        
class GenericMap[T]:
    size: DoubleNumber
    Map: list[list[T]]

    def __init__(self, size: DoubleNumber) -> None:
        self.size = size

    def __getitem__(self, index: int) -> list[T]:
        return self.Map[index]
    
    def get(self, pos: DoubleNumber) -> T:
        return self.Map[pos.y][pos.x]

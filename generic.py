from pygame import Surface
from textures import Texture
import pygame

# Needed for hp (or other things that have max value and are positive only)
class Alive:
    
    def __init__(self, maxValue: int, value: int = None):
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


# for money, resources and so on
class CountAble: 
    def __init__(self, value: float, income: float):
        self.value = value
        self.income = income
    # changes value. change can be negative also
    def change(self, value: float = None): 
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
        self.width, self.height = texture.width, texture.height
        
    # Counts frames and borders them by variable "frames"
    def nextFrame(self) -> None: 
        self.current = (self.current + 1) % self.frames
        
    # gives current frame's positions and size
    def getFrameCoords(self, curr: int = None) -> tuple[int, int, int, int]:
        if curr == None: curr = self.current 
        return (self.width * self.current, 0, self.width, self.height)
    
    # blits texture on display
    def blit(self, display: Surface, cords: tuple[int, int]) -> None:
        self.surface.blit(display, cords, self.getFrameCoords())
        
class GenericUnit(HasTexture, Alive):
    x: int
    y: int
    velocity_x: int
    velocity_y: int
    
    def __init__(self, texture: Texture, hp: int) -> None:
        HasTexture().__init__(texture)
        Alive().__init__(hp)
        
    def update(self, events: list[pygame.event.Event]):
        pass
    
    def draw(self, window: Surface):
        pass

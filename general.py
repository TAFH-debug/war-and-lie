from typing import Any
from pygame import Surface

class Alive:
    def __init__(self, value,  maxValue):
        self.value: int = value
        self.maxValue: int = maxValue
    def regenerate(self, value: int) -> None:
        self.value = min(self.value + value, self.maxValue)
    def gainDamage(self, value: int) -> bool:
        self.value -= value
        return self.isAlive()
    def isAlive(self) -> bool:
        return self.value > 0
    def __call__(self) -> int:
        return self.value
        

class Texture:
    def __init__(self, texture: Surface, size: tuple[int, int], frames: int = 1 ):
        self.texture: Surface = texture
        self.frames: int = frames
        self.current: int = 0
        self.width, self.height = size
    def nextFrame(self) -> None:
        self.current = (self.current + 1) % self.frames
    def getFrameCoords(self, curr: int = None) -> tuple[int, int, int, int]:
        if curr == None: curr = self.current 
        return (self.size[0] * self.current, 0, self.size[0], self.size[1])
    def blit(self, display: Surface, cords: tuple[int, int]) -> None:
        self.texture.blit(display, cords, self.getFrameCoords)
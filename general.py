from pygame import Surface

# Needed for hp (or other things that have max value and are positive only)
class Alive:
    def __init__(self, value,  maxValue):
        self.value: int = value
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
class Texture: 
    def __init__(self, texture: Surface, size: tuple[int, int], frames: int = 1 ):
        self.texture: Surface = texture
        self.frames: int = frames
        self.current: int = 0
        self.width, self.height = size
    # Counts frames and borders them by variable "frames"
    def nextFrame(self) -> None: 
        self.current = (self.current + 1) % self.frames
    # gives current frame's positions and size
    def getFrameCoords(self, curr: int = None) -> tuple[int, int, int, int]:
        if curr == None: curr = self.current 
        return (self.size[0] * self.current, 0, self.size[0], self.size[1])
    # blits texture on display
    def blit(self, display: Surface, cords: tuple[int, int]) -> None:
        self.texture.blit(display, cords, self.getFrameCoords)

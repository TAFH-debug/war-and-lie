import pygame
    

display: pygame.Surface = None

def draw():
    display.fill((0, 0, 0))
    

def update():
    pass

def init():
    display = pygame.display.set_mode((900, 1200))
    pygame.display.set_caption("ABOBA")

def game_cycle():
    draw()
    update()
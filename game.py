import pygame
from menu import *

display: pygame.Surface = None

def draw():
    display.fill((0, 0, 0))
    draw_all(display)
    
def update(events: list[pygame.event.Event]):
    pass

def init():
    global display
    display = pygame.display.set_mode((900, 1200))
    pygame.display.set_caption("ABOBA")
    
    add_menu("Main")
    

def game_cycle():
    while True:
        draw()
        events = pygame.event.get()
        update(events)

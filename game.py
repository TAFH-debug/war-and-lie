import pygame
from menu import *

display: pygame.Surface = None

def draw():
    display.fill((0, 0, 0))
    draw_all(display)
    
def update(events: list[pygame.event.Event]):
    update_all(events)

def init():
    global display
    display = pygame.display.set_mode((900, 1200))
    pygame.display.set_caption("ABOBA")
    pygame.font.init()
    
    add_menu("Main").add_widget(
        Label(500, 500, Text(
            "Hello!", pygame.font.SysFont("Arial", 60), (255, 0, 0)
        ))
    )
    
def game_cycle():
    draw()
    events = pygame.event.get()
    update(events)

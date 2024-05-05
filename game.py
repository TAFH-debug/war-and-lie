import pygame
from menu import *

display: pygame.Surface = None

def draw():
    display.fill((0, 0, 0))
    draw_all(display)
    pygame.display.flip()
    
def update(events: list[pygame.event.Event]):
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    update_all(events)

def init():
    global display
    display = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("War and lie")
    
    add_menu("Main").add_widget(
        Label(100, 100, Text(
            "Hello!", pygame.font.SysFont("Arial", 60), (255, 0, 0)
        ))
    )
    
def game_cycle():
    while True:
        draw()
        events = pygame.event.get()
        update(events)

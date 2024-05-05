import pygame
from .game import game_cycle, init


def main():
    pygame.init()
    pygame.font.init()
    init()
    game_cycle()
    
    
if __name__ == "__main__":
    main()
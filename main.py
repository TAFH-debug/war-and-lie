import pygame
from game import init, game_cycle


def main():
    pygame.init()
    init()
    game_cycle()
    
    
if __name__ == "__main__":
    main()
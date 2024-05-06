import pygame
import logging
from .game import game_cycle, init
from .exceptions import Warning

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s][%(name)s]: %(message)s"))
logger.addHandler(handler)


def main():
    logging.basicConfig()
    
    try:
        pygame.init()
        pygame.font.init()
        init()
        logging.info("Game initialized.")
        game_cycle()
    except Exception as e:
        logging.critical(e)
        exit(1)
    
    
if __name__ == "__main__":
    main()
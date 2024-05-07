import pygame
import logging
from .game import game_cycle, init, main_menu

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
        main_menu()
        game_cycle()
    except Exception as e:
        logging.critical(e.with_traceback(None))
        exit(1)
    
    
if __name__ == "__main__":
    main()
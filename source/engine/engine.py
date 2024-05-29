from source.engine import Scene
from .game_object import GameObject
import pygame as pg
import logging


class Engine:

    scenes: list[Scene]
    logger: logging.Logger
    display: pg.Surface

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s][%(name)s]: %(message)s"))
        self.logger.addHandler(handler)

    def register(self):
        pass

    def init(self, resolution: tuple[int, int]):
        pg.init()
        pg.font.init()
        logging.basicConfig()
        self.display = pg.display.set_mode(resolution)
        pg.display.set_caption(self.app_name)
        logging.info("Game initialized.")

    def run(self, resolution: tuple[int, int] = (800, 600)):
        self.init(resolution)

        try:
            self.cycle()
        except Exception as e:
            logging.critical(e.with_traceback(None))
            exit(1)

    def pygameEventProcessing(self, event):
        if event.type == pg.QUIT:
            logging.info("Quitting")
            exit()

    def cycle(self):
        while True:
            for event in pg.event.get():
                self.pygameEventProcessing(event)
            
            for i in GameObject.objects:
                i.update()

            for i in GameObject.objects:
                i.draw(self.display)

            pg.display.flip()

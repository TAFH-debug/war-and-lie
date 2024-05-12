from .widgets import *

widgets: dict[str, Menu] = dict()


def add_menu(nm: str):
    widgets[nm] = Menu(nm)
    return widgets[nm]


def draw_all(window: pygame.Surface):
    for v in widgets.values():
        v.draw(window)


def update_all(events: list[pygame.event.Event]):
    for v in widgets.values():
        v.update(events)


def get_menu(nm: str):
    return widgets[nm]

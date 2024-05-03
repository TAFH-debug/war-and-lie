from .widgets import *

widgets: dict[str, list[Widget]] = dict()

def add_menu(nm: str):
    widgets[nm] = []

def draw_all(window: pygame.Surface):
    for v in widgets.values():
        for k in v:
            k.draw(window)

def draw_menu(window, nm):
    for i in widgets[nm]:
        i.draw(window)

def update_menu(events, nm):
    for i in widgets[nm]:
        i.update(events)

def add_widget(nm, widget):
    widgets[nm].append(widget)
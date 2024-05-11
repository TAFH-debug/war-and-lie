import pygame


class Clicked:
    def __init__(self, color: tuple[int, int, int], border: "Border | None" = None):
        self.color = color
        self.border = border
    
    @staticmethod
    def get_default():
        return Clicked((0, 0, 0))

class Border:
    
    def __init__(self, width: int, color: tuple[int, int, int], radius: int):
        self.width = width
        self.color = color
        self.radius = radius
    
    @staticmethod
    def get_default():
        return Border(1, (0, 0, 0), -1)

class Text:

    def __init__(self, text: str, 
                 font: pygame.font.Font | None = None, 
                 color: tuple[int, int, int] = (0, 0, 0),
                 background_color: tuple[int, int, int] | None = None):
        font = font or pygame.font.SysFont("Arial", 20)
        self.text = text
        self.font = font
        self.color = color
        self.background_color = background_color
    
    def render(self):
        return self.font.render(self.text, False, self.color, self.background_color)
    
    @staticmethod
    def get_default():
        return Text('')
    
class RawWidget:
    """
    Abstract widget class.
    """    

    def __init__(self, x: int, y: int, width: int=100, height: int=100) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.childs: list[Widget] = []

    def draw(self, window: pygame.Surface):
        for i in self.childs:
            i.draw(window)

    def update(self, events: list[pygame.event.Event]):
        for i in self.childs:
            i.update(events)
            
class Widget(RawWidget):
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 clicked: Clicked | None=None, color=None, border: Border | None=None,
                 text: Text | None=None):
        super().__init__(x, y, width, height)        
        self.text = text
        self.border = border
        self.color = color
        self.clicked = clicked
        self.is_clicked = False
        
    def draw(self, window: pygame.Surface):
        super().draw(window)
        
        color = self.color
        border = self.border
        if self.clicked and self.is_clicked:
            color = self.clicked.color
            border = self.clicked.border
        
    
        if border:
            if color: 
                pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height), 0, border.radius)
            bw = border.width
            pygame.draw.rect(window, border.color, (self.x - bw, self.y - bw, self.width + bw, self.height + bw), bw, border.radius)
        elif color:
            pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))
        
        if self.text:
            txt = self.text.font.render(self.text.text, False, self.text.color)
            window.blit(txt, (self.x + (self.width - txt.get_width()) / 2, self.y + (self.height - txt.get_height()) / 2) + txt.get_size())

    def update(self, events: list[pygame.event.Event]):
        super().update(events)

        rc = pygame.Rect(self.x, self.y, self.width, self.height)
        for i in events:
            if i.type == pygame.MOUSEBUTTONDOWN and rc.collidepoint(pygame.mouse.get_pos()):
                self.is_clicked = True
            if i.type == pygame.MOUSEBUTTONUP and self.is_clicked:
                self.is_clicked = False
                self.onclick()
                
    def onclick(self):
        pass

class Label(Widget):
    """
    Shorthand name of widget that is used only as text.
    """
    
    def __init__(self, x, y, text: Text | None=None):
        self.text = text or Text.get_default()
        width, height = self.text.render().get_size()

        super().__init__(x, y, width, height, text=text)

    def draw(self, window: pygame.Surface):
        super().draw(window)

    def update(self, events):
        super().update(events)


class Button(Widget):
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 clicked: Clicked | None=None, color=(255, 0, 0), border: Border | None=None, cmd=lambda: (), 
                 text: Text | None=None, data=None):
        
        Widget.__init__(self, x, y, width, height, clicked, color, border, text)
        self.cmd = cmd
        self.data = data

    def onclick(self):
        self.cmd(self.data)
                
class Menu:
    is_disabled: bool
    widgets: list[Widget]
    name: str
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_disabled = False
        self.widgets = []
        
    def add_widget(self, widget: Widget):
        self.widgets.append(widget)
        
    def draw(self, window: pygame.Surface):
        if self.is_disabled: return
        for i in self.widgets:
            i.draw(window)
            
    def update(self, events: list[pygame.event.Event]):
        if self.is_disabled: return
        for i in self.widgets:
            i.update(events)
            
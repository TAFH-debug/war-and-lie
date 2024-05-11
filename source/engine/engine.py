from typing import TypeVar
from vmath import *


class Component:
    game_object: "GameObject"
    
    def __init__(self, obj: "GameObject"):
        self.game_object = obj
        
    def draw(self):
        pass
    
    def update(self):
        pass
    
    def destroy(self):
        pass


class Transform:
    game_object: "GameObject"
    position: Vector2d # position of CENTER
    angle: Angle
    childs: list["Transform"]
    
    def __init__(self, obj: "GameObject"):
        self.game_object = obj
        self.position = Vector2d(0, 0)
        
    def translate(self, trn: Vector2d):
        self.position += trn
        for child in self.childs:
            child.translate(trn)
        
    def rotate(self, angle: Angle):
        self.angle += angle
        # TODO rotate all of the childs relative to center of this transform.
        
    def add_child(self, child: "Transform"):
        self.childs.append(child)
    
T = TypeVar("T", bound=Component)

"""
Inspired by Unity.
"""
class GameObject:
    components: list[Component]
    active: bool
    tag: str
    transform: Transform
    childs: list["GameObject"]
    
    objects: list["GameObject"] = []
    
    def __init__(self, tag: str):
        self.components = []
        self.active = True
        self.tag = tag
        GameObject.objects.append(self)
    
    def draw(self):
        for i in self.components:
            i.draw()
    
    def update(self):
        for i in self.components:
            i.update()
    
    def on_destroy(self):
        for i in self.childs:
            GameObject.destroy(i)
        
    def add_component(self, component: type[T]):
        self.components.append(component(self))
        
    def get_component(self, component: type[T]) -> T:
        for i in self.components:
            if isinstance(i, component):
                return i
        raise Exception("No such component")
    
    def set_active(self, active: bool):
        self.active = active
    
    @staticmethod
    def get_by_tag(tag: str) -> "GameObject":
        for i in GameObject.objects:
            if (i.tag == tag):
                return i
        raise Exception("No such object")
            
    @staticmethod
    def destroy(obj: "GameObject"):
        obj.on_destroy()
        del obj


class Engine:
    
    def __init__(self, app_name: str):
        self.app_name = app_name
    
    def register(self):
        pass
    
    def run(self):
        pass
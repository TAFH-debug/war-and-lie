class Scene:
    name: str
    prefabs: list[Prefab]
    
    def __init__(self, name: str):
        self.name = name

    def init(self):
        pass

    def draw(self, window):
        pass

    def update(self, events):
        pass

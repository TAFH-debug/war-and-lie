from .resources import Cost
from .building import BuildingTypes, BuildingType

class Tech:
    def __init__(self, id: str = "wal:tech:none", research_time: int = 0, cost: Cost = Cost({}), completed: bool = False, unlock: tuple[BuildingType] = []):
        self.id = id
        self.research_time = research_time
        self.cost = cost
        self.completed = completed
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class TechTypes:
    """
    Here may be all techs in the game
    """
    nature = Tech(id="wal:tech:nature_root", completed=True, unlock=(BuildingTypes.shipYard))

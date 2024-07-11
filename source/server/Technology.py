from .resources import Cost
from .building import BuildingTypes, BuildingType

from server.vmath import to_bytes


class Tech:
    id: int
    name: str
    research_time: int
    cost: Cost
    completed: bool
    children: list["Tech"]

    idCount = 0

    def __init__(self, name: str = "wal:tech:none", research_time: int = 0, cost: Cost = Cost({}), completed: bool = False, children: list["Tech"] = [], unlock: tuple[BuildingType] = []):
        self.id = Tech.idCount
        Tech.idCount += 1
        self.name = name
        self.research_time = research_time
        self.cost = cost
        self.completed = completed
        self.children = children
        self.unlock = unlock

    def add_child(self, child):
        self.children.append(child)

    def as_bytes(self) -> bytes:
        return to_bytes(self.id)
    
    def __repr__(self) -> str:
        return f"Ttype = {self.name}"

class TechTypes:
    """
    Here may be all techs in the game
    """
    nature = Tech(name="wal:tech:nature_root", completed=True, unlock=(BuildingTypes.shipYard))

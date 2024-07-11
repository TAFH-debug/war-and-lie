from  server.vmath import *
from .generic import CountAble, GenericObject

class ResourceType:
    name: str
    idCount = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self.index = ResourceType.idCount
        ResourceType.idCount += 1


    def as_bytes(self) -> bytes:
        return to_bytes(self.index)
    
    def __repr__(self) -> str:
        return f"Rtype = {self.name}"
# Основной класс для ресурсов
class Resource(CountAble):
    resourceType: ResourceType
    initial_amount: int
    income: int

    def __init__(self, resourceType: ResourceType, initial_amount: int, income: int) -> None:
        CountAble.__init__(self, initial_amount, income)
        self.resourceType = resourceType


    def increase(self, amount: int | None = None) -> None:
        if amount == None:
            self.change()
        else:
            self.change(self.value + amount)

    def decrease(self, amount: int) -> None:
        self.change(max(self.value - amount, 0))
    
    def as_bytes(self) -> bytes:
        return merge(CountAble.as_bytes(self), ResourceType.as_bytes(self))

    def __repr__(self) -> str:
        return f"RESOURCE: <{self.resourceType}, {CountAble.__repr__(self)}"

class ResourceTypes:
    """
    Here ought to be all resources in the game
    """

    wood = ResourceType("Wood")
    
    allResources: list[ResourceType] = [wood]
# Класс для шахт и деревьев
class ResourceSource(GenericObject):
    name: str
    production_rate: int

    id:int
    idCount = 0

    def __init__(self, name: str, pos: Vector2d, production_rate: int) -> None:
        GenericObject.__init__(self)
        self.id = ResourceSource.idCount
        ResourceSource.idCount += 1
        self.name = name
        self.pos = pos
        self.production_rate = production_rate
        self.timer = 0

    def update(self) -> bool:
        # Обновляем количество ресурсов
        self.timer += 1
        if self.timer == self.production_rate:
            self.timer = 0
            return True
        return False

    def as_bytes(self) -> bytes:
        return merge(GenericObject.as_bytes(self), to_bytes(bytes(self.id, )))
    
    def __repr__(self) -> str:
        return f"RESOURCE_SOURCE: <RStype = {self.name}, {GenericObject.__repr__(self)}>"

class Cost:
    costs: dict[ResourceType, int]

    def __init__(self, costs: dict[ResourceType: int]) -> None:
        self.costs = costs

    def doesFit(self, resources: list[Resource]) -> bool:
        for resource in resources:
            if self.costs[resource] > resource.value:
                return False
        return True

    def buy(self, resources: list[Resource]) -> bool:
        for resource in resources:
            if self.costs[resource] < resource.value:
                resource.decrease(self.costs[resource])
            else:
                return False
        return True
    
    def as_bytes(self) -> bytes:
        return to_bytes((merge(resource.as_bytes(), to_bytes(self.costs[resource])) for resource in self.costs))

    def __repr__(self) -> str:
        return f"cost = {[f"{Rtype}:{self.costs[Rtype]}" for Rtype in self.costs]}"

# Класс для покупки
class Services:
    services: dict[str, Cost]

    def __init__(self) -> None:
        self.services: dict[str, Cost] = {}  # список доступных покупок

    def add_service(self, name: str, cost: Cost) -> None:
        self.services[name] = cost

    def buy_service(self, resources: list[Resource], service_name: str) -> bool:
        if service_name in self.services:
            cost: Cost = self.services[service_name]
            return cost.buy(resources)
        else:
            return False
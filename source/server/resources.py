from source.vmath import *
from .generic import CountAble, GenericObject

class ResourceType:
    name: str
    index: int
    # index to access to resources easily. for example: wood is 0 iron is 1 stone is 2
    # and in c++ or java we could make it with static, but python...
    # soon there will be something about generation on map

    def __init__(self, name: str, index: int) -> None:
        self.name = name
        self.index = index

# Основной класс для ресурсов
class Resource(CountAble):
    name: str
    index: int
    initial_amount: int
    income: int

    def __init__(self,resourceType: ResourceType, initial_amount: int, income: int) -> None:
        CountAble.__init__(self, initial_amount, income)
        self.name = resourceType.name
        self.index = resourceType.index


    def increase(self, amount: int | None = None) -> None:
        if amount == None:
            self.change()
        else:
            self.change(self.value + amount)

    def decrease(self, amount: int) -> None:
        self.change(max(self.value - amount, 0))


class ResourceTypes:
    """
    Here ought to be all resources in the game
    """

    wood = ResourceType("Wood", 0)
    
    allResources: list[ResourceType] = [wood]
# Класс для шахт и деревьев
class ResourceSource(GenericObject):
    name: str
    color: tuple[int, int, int]
    production_rate: int

    def __init__(self, id: str, name: str, color: tuple[int, int, int], pos: Vector2d, production_rate: int) -> None:
        GenericObject.__init__(self)
        self.id = id
        self.name = name
        self.color = color
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


class Cost:
    costs: dict[ResourceType: int]

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
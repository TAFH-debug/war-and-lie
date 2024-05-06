import pygame
import sys
import random
from generic import CountAble

pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD_COLOR = (255, 215, 0)  # Цвет для золота
IRON_COLOR = (169, 169, 169)  # Цвет для железа
WOOD_COLOR = (34, 139, 34)  # цвет для деревьев


# Основной класс для ресурсов
class Resource(CountAble):
    def __init__(self, name, color, initial_amount, income):
        super().__init__(initial_amount, income)
        self.name = name
        self.color = color

    def increase(self, amount=None):
        if amount is None:
            self.change()
        else:
            self.change(self.value + amount)

    def decrease(self, amount):
        self.change(max(self.value - amount, 0))

# Класс для шахт и деревьев
class ResourceSource:
    def __init__(self, name, color, position, production_rate):
        self.name = name
        self.color = color
        self.position = position
        self.production_rate = production_rate
        self.timer = 0

    def update(self):
        # Обновляем количество ресурсов
        self.timer += 1
        if self.timer >= self.production_rate:
            self.timer = 0
            return True
        return False

# Класс для покупки
class Services:
    def __init__(self):
        self.services = {}#cписок доступных покупок

    def add_service(self, name, cost):
        self.services[name] = cost

    def buy_service(self, resource, service_name):
        if service_name in self.services:
            cost = self.services[service_name]
            if resource.value >= cost:
                resource.change(resource.value - cost)
                print("Приобретена:", service_name)
            else:
                print("Недостаточно ресурсов")
        else:
            print("Error")


services = Services()

# Example услуг
services.add_service("Healing", 20)
services.add_service("Upgrade", 50) 

# Создание ресурсов
gold = Resource("Gold", GOLD_COLOR, 100, 0)
iron = Resource("Iron", IRON_COLOR, 50, 0)
wood = Resource("Wood", WOOD_COLOR, 80, 0)

# Создание шахт
gold_mine = ResourceSource("Gold Mine", GOLD_COLOR, (300, 200), 100)  # Генерация золота каждые 100 кадров
iron_mine = ResourceSource("Iron Mine", IRON_COLOR, (400, 400), 150)  # Генерация железа каждые 150 кадров

# Создание деревьев
wood_forests = []
for _ in range(3):
    position = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
    wood_forest = ResourceSource("Wood Forest", WOOD_COLOR, position, 120)
    wood_forests.append(wood_forest)

# Exampe отрисовки и т.д.
#while True:
#    screen.fill(WHITE)
#    if gold_mine.update():
#        gold.increase(1)
#    if iron_mine.update():
#        iron.increase(1)
#    for wood_forest in wood_forests:
#        if wood_forest.update():
#            wood.increase(1)
#
#    # Отображение ресурсов на экране
#    pygame.draw.rect(screen, gold.color, (50, 50, gold.value, 20))
#    pygame.draw.rect(screen, iron.color, (50, 100, iron.value, 20))
#    pygame.draw.rect(screen, wood.color, (50, 150, wood.value, 20))
#
#    # Отображение надписей рядом с ресурсами
#    gold_text = font.render(gold.name + ": " + str(gold.value), True, BLACK)
#    iron_text = font.render(iron.name + ": " + str(iron.value), True, BLACK)
#    wood_text = font.render(wood.name + ": " + str(wood.value), True, BLACK)
#    screen.blit(gold_text, (200, 50))
#    screen.blit(iron_text, (200, 100))
#    screen.blit(wood_text, (200, 150))
#
#    # Отображение источников ресурсов
#    pygame.draw.circle(screen, gold_mine.color, gold_mine.position, 10)
#    pygame.draw.circle(screen, iron_mine.color, iron_mine.position, 10)
#    for wood_forest in wood_forests:
#        pygame.draw.circle(screen, wood_forest.color, wood_forest.position, 10)
#
#    pygame.display.flip()

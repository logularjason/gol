import pygame as pg
import random 
import math

class Food:
    def __init__(self, screen, width, height, energy):
        self.screen = screen
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.energy = energy

    def draw(self):
        pg.draw.rect(self.screen, "black", [self.x-2, self.y-2, 8, 8], 2) # left, top, width, height

    # return distance to creature
    def distance(self, creature):
        dx = self.x - creature.x
        dy = self.y - creature.y
        return math.sqrt(dx * dx + dy * dy)

    # return the direction of the food
    def direction(self, creature):
        dx = self.x - creature.x
        dy = self.y - creature.y
        return math.atan2(dy, dx)

class Foodlist:
    def __init__(self, screen, creatureList, energy, width, height, factor):
        self.screen = screen
        self.creatureList = creatureList
        self.energy = energy
        self.width = width
        self.height = height
        self.factor = factor
        self.foodlist = []
        self.spawn()

    def draw(self):
        for food in self.foodlist:
            food.draw()

    # Return the nearest food to the the supplied creature
    def nearest(self, creature):
        bestFood = None
        bestDistance = float('inf') # start with infinity - this is wierd syntax BTW
        for food in self.foodlist:
            d = food.distance(creature)
            if (d < bestDistance):
                bestDistance = d
                bestFood = food
        return bestFood

    # remove food from our list
    def spawn(self):
        for c in range(len(self.foodlist), int(len(self.creatureList.creatures) * self.factor)):
            self.foodlist = self.foodlist + [Food(self.screen, self.width, self.height, self.energy)]

    # remove food from our list
    def respawn(self, food):
        self.foodlist.remove(food)
        self.spawn()
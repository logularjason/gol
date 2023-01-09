import pygame as pg
import random 
import math
from constants import *

class Food:
    def __init__(self, screen, x = None, y = None):
        self.screen = screen
        if x is None:
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(0, SCREEN_HEIGHT)
            self.colour = "black"
        else:
            self.x = x 
            self.y = y
            self.colour = "red"
        self.energy = CREATURE_STARTING_ENERGY

    def draw(self):
        pg.draw.rect(self.screen, self.colour, [self.x-4, self.y-4, 8, 8], 2) # left, top, width, height



    # return distance to creature
    def distance(self, creature):
        smell = creature.dna.smell
        dx = self.x - creature.x
        dy = self.y - creature.y
        normalisedSmell = ((smell - NORMALISED_GENE_MIN) / NORMALISED_GENE_RANGE) 
        smellCostFactor = (1 - normalisedSmell) * SMELL_FACTOR + (1 - SMELL_FACTOR)
        distance = math.sqrt(dx * dx + dy * dy)
        #print ("smell =", smell, "normalisedSmell = ", normalisedSmell, " smellCostFactor =", smellCostFactor)
        return distance * smellCostFactor 

    # return the direction of the food
    def direction(self, creature):
        smell = creature.dna.smell
        dx = self.x - creature.x
        dy = self.y - creature.y
        normalisedSmell = ((smell - NORMALISED_GENE_MIN) / NORMALISED_GENE_RANGE) 
        smellCostFactor = (1 - normalisedSmell) * SMELL_FACTOR + (1 - SMELL_FACTOR)
        return math.atan2(dy, dx)+ (smellCostFactor * random.randint(-1, 1))

class Foodlist:
    def __init__(self, screen, creatureList):
        self.screen = screen
        self.creatureList = creatureList
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

    # spawn new food to keep a constant supply
    def spawn(self):
        for c in range(len(self.foodlist), FOOD_COUNT):
            self.foodlist = self.foodlist + [Food(self.screen)]

    # remove food from our list
    def respawn(self, food):
        self.foodlist.remove(food)
        self.spawn()
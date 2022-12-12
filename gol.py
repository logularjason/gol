# Using pygame for graphics.  See this tutorial:
# https://www.pygame.org/docs/ref/draw.html
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random 
import math


# A class to model the traits of a creature
class DNA:

    # Create new DNA.  We use the parent DNA if it is passed to the constructor
    # Note that parentDna has a default of None if no argument is passed
    def __init__(self, parentDna = None):
        if parentDna is None:
            self.hopDistance = random.randint(1, 50)
        else:
            self.hopDistance = parentDna.hopDistance # Use the parent's DNA

# Hold the energy of a creature and provide methods to calculate
# changes to energy based on movement, etc.
class Energy:

    # Create new DNA
    def __init__(self):
        self.energy = 200

    # Update our health based on move distance - moving has a cost
    def updateEnergy(self, mx, my):
        self.energy = self.energy - math.sqrt(mx*mx + my*my)


# A class to represent a creature 
class Creature:

    # Constructor to create a new creature
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)
        self.dna = DNA()
        self.energy = Energy()
        self.draw()
   
    def draw(self):
        # area = pi * r ^ 2
        pg.draw.circle(self.screen, "blue", [self.x, self.y], math.sqrt(self.energy.energy))

    # Calculate our move vector based on our hopDistance
    # Return whether the creature passed over the food
    def calculateMoveVector(self, direction, distance):
        self.mx = self.dna.hopDistance * math.cos(direction)
        self.my = self.dna.hopDistance * math.sin(direction)

        # Limit mx and my to not let the creature move out of bounds
        if (self.x + self.mx > 999):
            self.mx = 999 - self.x
        if (self.x + self.mx < 1):
            self.mx = self.x - 1
        if (self.y + self.my > 999):
            self.my = 999 - self.y
        if (self.y + self.my < 1):
            self.my = self.y - 1

        # Update our location
        self.x = self.x + self.mx
        self.y = self.y + self.my
        didHopOverFood = (self.dna.hopDistance >= distance)
        return didHopOverFood

    # Move and die if no energy left
    def move(self, foodlist):
        # Get details of the food, direction, and whether we got the food
        nearestFood = foodlist.nearest(self)
        distance = nearestFood.distance(self)
        direction = nearestFood.direction(self)
        didHopOverFood = self.calculateMoveVector(direction, distance)
        print('cx={} cy={} fx={} fy={} mx={} my={} angle={:2.2} energy={}'.format(self.x, self.y, nearestFood.x, nearestFood.y, self.mx, self.my, direction, self.energy.energy))

        self.energy.updateEnergy(self.mx, self.my)

        # Move if we have enerty or die
        if self.energy.energy > 0:
            self.draw()
            if (didHopOverFood is True):
                self.eat(foodlist, nearestFood)
            return True
        else:
            return False

    def eat(self, foodlist, food):
        self.energy.energy = self.energy.energy + food.energy
        foodlist.remove(food)
        
class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)
        self.energy = 250

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
    def __init__(self, screen):
        self.screen = screen
        self.foodlist = []
        for c in range(25):
            self.foodlist = self.foodlist + [Food(screen)]

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

    # remove food from our list and also cavas
    def remove(self, food):
        self.foodlist.remove(food)
    

# Create a list of creatures
def createCreatures(screen, creatureCount):
    # This is a local variable containing an empty list
    # Read up on lists and tuples; e.g. https://realpython.com/python-lists-tuples/
    creatures = []
    # Repeatedly create creatures
    # Each creature is created with a different location and appended to our list
    # See how it's possible to use '+' to append lists?
    for c in range(creatureCount):
        creatures = creatures + [Creature(screen)]
    # Return the list to the caller
    return creatures

# ==========================================
# This function runs the script
# ==========================================
def main():
    pg.init()
    # Set the height and width of the screen
    size = [1000, 1000]
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Lauras World")
    # Create a list of creatures
    creatures = createCreatures(screen, 20)
    foodlist = Foodlist(screen)
    # Move the creatures
    # moveCreatures(window, screen, creatures, foodlist)

    done = False
    clock = pg.time.Clock()

    while not done:
        # This limits the while loop to a max of n times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(5)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        screen.fill("white")
        foodlist.draw()
        # Move each creature
        for creature in creatures:
            didMove = creature.move(foodlist)
            if didMove is False:
                creatures.remove(creature)
        pg.display.flip()

    pg.quit()
    quit()


if __name__ == "__main__":
    main()
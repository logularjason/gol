import random 
import math
import pygame as pg
startEnergy=1000

# A class to model the traits of a creature
class DNA:

    # Create new DNA.  We use the parent DNA if it is passed to the constructor
    # Note that parentDna has a default of None if no argument is passed
    def __init__(self, parentDna = None):
        if parentDna is None:
            self.hopDistance = random.randint(1, 50)
        else:
            self.hopDistance = parentDna.hopDistance # Use the parent's DNA

    def colour(self):
        return "blue"

# Hold the energy of a creature and provide methods to calculate
# changes to energy based on movement, etc.
class Energy:

    # Create new DNA
    def __init__(self, startEnergy):
        self.energy = startEnergy

    # Update our health based on move distance - moving has a cost
    def updateEnergy(self, mx, my):
        self.energy = self.energy - math.sqrt(mx*mx + my*my)


# A class to represent a creature 
class Creature:

    # Constructor to create a new creature
    def __init__(self, screen, width, height, startEnergy):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.dna = DNA()
        self.energy = Energy(startEnergy)
        self.draw()
   
    def draw(self):
        # area = pi * r ^ 2
        pg.draw.circle(self.screen, self.dna.colour(), [self.x, self.y], math.sqrt(self.energy.energy))

    # Calculate our move vector based on our hopDistance
    # Return whether the creature passed over the food
    def calculateMoveVector(self, direction, distance):
        self.mx = self.dna.hopDistance * math.cos(direction)
        self.my = self.dna.hopDistance * math.sin(direction)

        # Limit mx and my to not let the creature move out of bounds
        if (self.x + self.mx > self.width):
            self.mx = self.width - self.x - 1
        if (self.x + self.mx < 1):
            self.mx = self.x - 1
        if (self.y + self.my > self.height):
            self.my = self.height - self.y - 1
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
        foodlist.respawn(food)

class CreatureList:

    # Constructor to create a new creature
    def __init__(self, screen, width, height, creatureCount, startEnergy):
        self.screen = screen
        self.width = width
        self.height = height
        self.creatureCount = creatureCount
        self.startEnergy = startEnergy
        self.creatures = []
        # Repeatedly create creatures
        # Each creature is created with a different location and appended to our list
        # See how it's possible to use '+' to append lists?
        for c in range(creatureCount):
            self.creatures = self.creatures + [Creature(screen, self.width, self.height, self.startEnergy)]

    def move(self, foodlist):
        # Move each creature
        for creature in self.creatures:
            didMove = creature.move(foodlist)
            if didMove is False:
                self.creatures.remove(creature)


    def replicate(threshold, energy):
        for creature in CreatureList:
            if (energy >= threshold):
                creature.energy = startEnergy 
                CreatureList.append(creature)
    


        # loop over all creatures, if theyre energy is above threshold, then create new creature and put it in the list 
        # i will need to figure out how to create a new creature with the right energy and DNA and fix parent energy 

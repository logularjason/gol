import random 
import math
import pygame as pg
from constants import *
from dna import *
from energy import *
from food import *


# A class to represent a creature 
class Creature:

    serialNumber = 1

    # Constructor to create a new creature
    def __init__(self, screen, parent = None):
        self.screen = screen
        self.id = Creature.serialNumber
        self.age = 1
        Creature.serialNumber+=1
        if (parent is None):
            # Generate random properties
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(0, SCREEN_HEIGHT)
            self.dna = DNA()
            self.energy = Energy()
            self.parent = None
        else:
            # Base our properties on the parent properties
            self.dna = DNA(parent.dna)
            self.energy = Energy(parent.energy.energy * ENERGY_SPLITTING_FACTOR)
            self.x = parent.x + random.randint(CREATURE_REPLICATION_DISTANCE, CREATURE_REPLICATION_DISTANCE)
            self.y = parent.y + random.randint(CREATURE_REPLICATION_DISTANCE, CREATURE_REPLICATION_DISTANCE)
            self.parent = parent
        self.draw()
   
    def distance(self, creature):
        dx = self.x - creature.x
        dy = self.y - creature.y
        return math.sqrt(dx * dx + dy * dy)

    # draw the creature varying colour, opacity, radius
    def draw(self):
        colour = self.fillColour() # colour depends on DNA and opacity depends on energy
        opacity = colour.a
        radius=CREATURE_RADIUS
        if (opacity < 75):
            radius=radius*opacity/75 # if we have low opacity shrink the radius
        # Need a surface to support opacity
        surface1 = pg.Surface((radius*2, radius*2))
        surface1.set_colorkey("black")
        surface1.set_alpha(opacity)
        # Draw the circle on the surface
        pg.draw.circle(surface1, colour, [radius, radius], radius)
        # Put the surface on the screen
        self.screen.blit(surface1, [self.x-radius, self.y-radius])

        # Draw a border around the circle whose colour and thickness vary
        pg.draw.circle(self.screen, self.borderColour(), [self.x, self.y], radius, width=self.borderThickness())
        self.age += 1


    # colour depends on DNA and opacity depends on energy
    def fillColour(self):
        red=self.calculateColorValue(self.dna.hopDistance)
        green=self.calculateColorValue(self.dna.stamina)
        blue=self.calculateColorValue(self.dna.smell)
        opacity = int(self.energy.energy * ENERGY_OPACITY_FACTOR)
        if (opacity > 255):
            opacity = 255
        # print('r={} g={} b={} a={}'.format(red, green, blue, opacity))
        return pg.Color(red, green, blue, opacity)

    # calculate one of r, g or b and ensure the value is clipped to (0,255)
    def calculateColorValue(self, gene):
        value = (gene-NORMALISED_GENE_MIN) * 255 / NORMALISED_GENE_RANGE
        if value < 0:
            return 0
        else:
            if value > 255:
                return 255
            else:
                return int(value)

    # The colour of the border around the circle
    def borderColour(self):
        # Laura TBD - suggest change the colour based on whether we have been poisoned.
        return "black"

    # The thickness of the border
    def borderThickness(self):
        # Laura TBD - suggest change the thickness based on whether we have been poisoned.
        return 1

    # Calculate our move vector based on our hopDistance
    # Return whether the creature passed over the food
    def calculateMoveVector(self, direction, distance):
        self.mx = self.dna.hopDistance * math.cos(direction)
        self.my = self.dna.hopDistance * math.sin(direction)

        # Limit mx and my to not let the creature move out of bounds
        if (self.x + self.mx > SCREEN_WIDTH):
            self.mx = SCREEN_WIDTH - self.x - 1
        if (self.x + self.mx < 1):
            self.mx = self.x - 1
        if (self.y + self.my > SCREEN_HEIGHT):
            self.my = SCREEN_HEIGHT - self.y - 1
        if (self.y + self.my < 1):
            self.my = self.y - 1

        # Update our location
        self.x = self.x + self.mx
        self.y = self.y + self.my
        didHopOverFood = (self.dna.hopDistance >= distance)
        return didHopOverFood

    # Reduce our energy based on the poison value passed
    def poison(self, poison):
        newenergy = self.energy.energy - poison
        self.energy.energy = newenergy
        # Laura TBD - suggest store the age we were poisoned here
        print('Poison id={} energy={} poison={}'.format(self.id, self.energy.energy, poison))

    # Move and die if no energy left
    def move(self, foodlist, creaturelist):
        # Get details of the food, direction, and whether we got the food
        nearestFood = foodlist.nearest(self)
        distance = nearestFood.distance(self)
        direction = nearestFood.direction(self)
        didHopOverFood = self.calculateMoveVector(direction, distance)
        # print('cx={} cy={} fx={} fy={} mx={} my={} angle={:2.2} energy={}'.format(self.x, self.y, nearestFood.x, nearestFood.y, self.mx, self.my, direction, self.energy.energy))

        self.energy.updateEnergy(self.mx, self.my, self.dna.stamina)

        nearestCreature = creaturelist.nearest(self)
        # Don't poison our offspring
        if nearestCreature is not None and nearestCreature is not self.parent:
            nearestCreature.poison(self.dna.poison)

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

# A class to represent a list of creatures
class CreatureList:

    # Constructor to create a new creature
    def __init__(self, screen):
        self.screen = screen
        self.creatures = []
        # Repeatedly create creatures
        for c in range(CREATURE_COUNT):
            self.creatures = self.creatures + [Creature(screen)]

    # Move creatures including eating and death checks
    def move(self, foodlist):
        # Move each creature
        for creature in self.creatures:
            didMove = creature.move(foodlist, self)
            if didMove is False:
                self.creatures.remove(creature)
                newFood = Food(foodlist.screen, creature.x, creature.y)
                foodlist.foodlist.append(newFood)
            
    # return the creature nearest to the one specified or None creature is too far away
    def nearest(self, creature):
        bestCreature = None
        bestDistance = float('inf') # start with infinity - this is wierd syntax BTW
        otherCreatures = self.creatures.copy()
        otherCreatures.remove(creature)
        for c in otherCreatures:
            d = c.distance(creature)
            if (d < bestDistance):
                bestDistance = d
                bestCreature = c
        if bestDistance < POISON_MAX_DISTANCE:
            return bestCreature
        else:
            return None

    # Replicate healthy creatures
    def replicate(self):
        for creature in self.creatures:
            if (creature.energy.energy >= REPLICATION_HEALTH_THRESHOLD):
                splitEnergy = creature.energy.energy * ENERGY_SPLITTING_FACTOR
                creature.energy.energy = splitEnergy
                offspring = Creature(self.screen, creature)
                self.creatures.append(offspring)
                offspring.dna.printGenes('Replicate offspring', offspring.id)

    # Get DNA values for plotting them
    def dnaData(self):
        hopGenes = []
        smellGenes = []
        staminaGenes = []
        poisonGenes = []
        for creature in self.creatures:
            hopGenes.append(creature.dna.hopDistance)
            smellGenes.append(creature.dna.smell)
            staminaGenes.append(creature.dna.stamina)
            poisonGenes.append(creature.dna.poison)
        return [hopGenes, staminaGenes, smellGenes, poisonGenes]

    # Get energy values for plotting them
    def energyData(self):
        energyList = []
        for creature in self.creatures:
            energyList.append(creature.energy.energy)
        return energyList
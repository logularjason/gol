import random 
import math
import pygame as pg
from constants import *

# A class to model the traits of a creature
class DNA:

    # Create new DNA.  We use the parent DNA if it is passed to the constructor
    # Note that parentDna has a default of None if no argument is passed
    def __init__(self, parentDna = None):
        if parentDna is None:
            self.generateDna()
        else:
            self.replicateDna(parentDna)

    # generate DNA which totals to 100
    # each gene is a fractionof this 100
    def generateDna(self):
        hopDistance = random.randint(MIN_GENE, MAX_GENE)
        smell = random.randint(MIN_GENE, MAX_GENE)
        stamina = random.randint(MIN_GENE, MAX_GENE)
        normalise = 100 / (hopDistance + smell + stamina)
        self.hopDistance = hopDistance * normalise
        self.smell = smell * normalise
        self.stamina = stamina * normalise

    # Add fuzz to each parent gene, then normalise back so that total is still 100
    def replicateDna(self, parentDna):
        hopDistance = parentDna.hopDistance + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        smell = parentDna.smell + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        stamina = parentDna.stamina + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        normalise = 100 / (hopDistance + smell + stamina)
        self.hopDistance = hopDistance * normalise
        self.smell = smell * normalise
        self.stamina = stamina * normalise

# Hold the energy of a creature and provide methods to calculate
# changes to energy based on movement, etc.
class Energy:

    # Create new Energy
    def __init__(self, suppliedEnergy = None):
        if (suppliedEnergy is None):
            self.energy = CREATURE_STARTING_ENERGY
        else:
            self.energy = suppliedEnergy

    # Update our health based on move distance - moving has a cost
    def updateEnergy(self, mx, my, stamina):
        correctedStamina = (1 - ((stamina - NORMALISED_GENE_MIN) / NORMALISED_GENE_RANGE)) + STAMINA_OFFSET
        self.energy = self.energy - math.sqrt(mx*mx + my*my) * correctedStamina
        print('self.energy={} stamina={} correctedStamina={}'.format(self.energy, stamina, correctedStamina))


# A class to represent a creature 
class Creature:

    # Constructor to create a new creature
    def __init__(self, screen, parent = None):
        self.screen = screen
        if (parent is None):
            # Generate random properties
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(0, SCREEN_HEIGHT)
            self.dna = DNA()
            self.energy = Energy()
        else:
            # Base our properties on the parent properties
            self.dna = DNA(parent.dna)
            self.energy = Energy(parent.energy.energy * ENERGY_SPLITTING_FACTOR)
            self.x = parent.x + random.randint(CREATURE_REPLICATION_DISTANCE, CREATURE_REPLICATION_DISTANCE)
            self.y = parent.y + random.randint(CREATURE_REPLICATION_DISTANCE, CREATURE_REPLICATION_DISTANCE)
        self.draw()
   
    # draw the creature varying colour, opacity, radius
    def draw(self):
        colour = self.colour() # colour depends on DNA and opacity depends on energy
        opacity = colour.a
        radius=CREATURE_RADIUS
        if (opacity < 75):
            radius=radius*opacity/75 # if we have low opacity shrink the radius
        # Need a surface to support opacity
        surface1 = pg.Surface((radius*2,radius*2))
        surface1.set_colorkey("black")
        surface1.set_alpha(opacity)
        # Draw the circle on the surface
        pg.draw.circle(surface1, colour, [radius, radius], radius)
        # Put the surface on the screen
        self.screen.blit(surface1, [self.x-radius, self.y-radius])

    # colour depends on DNA and opacity depends on energy
    def colour(self):
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

    # Move and die if no energy left
    def move(self, foodlist):
        # Get details of the food, direction, and whether we got the food
        nearestFood = foodlist.nearest(self)
        distance = nearestFood.distance(self)
        direction = nearestFood.direction(self)
        didHopOverFood = self.calculateMoveVector(direction, distance)
        # print('cx={} cy={} fx={} fy={} mx={} my={} angle={:2.2} energy={}'.format(self.x, self.y, nearestFood.x, nearestFood.y, self.mx, self.my, direction, self.energy.energy))

        self.energy.updateEnergy(self.mx, self.my, self.dna.stamina)

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
            didMove = creature.move(foodlist)
            if didMove is False:
                self.creatures.remove(creature)

    # Replicate healthy creatures
    def replicate(self):
        for creature in self.creatures:
            if (creature.energy.energy >= REPLICATION_HEALTH_THRESHOLD):
                splitEnergy = creature.energy.energy * ENERGY_SPLITTING_FACTOR
                creature.energy.energy = splitEnergy
                offspring = Creature(self.screen, creature)
                self.creatures.append(offspring)

    # Get DNA values for plotting them
    def dnaData(self):
        hopGenes = []
        smellGenes = []
        staminaGenes = []
        for creature in self.creatures:
            hopGenes.append(creature.dna.hopDistance)
            smellGenes.append(creature.dna.smell)
            staminaGenes.append(creature.dna.stamina)
        return [hopGenes, smellGenes, staminaGenes]

    # Get energy values for plotting them
    def energyData(self):
        energyList = []
        for creature in self.creatures:
            energyList.append(creature.energy.energy)
        return energyList
import random 
import math
import pygame as pg
from constants import *
from food import *

# A class to model the traits of a creature
class DNA:

    # Create new DNA.  We use the parent DNA if it is passed to the constructor
    # Note that parentDna has a default of None if no argument is passed
    def __init__(self, parentDna = None):
        if parentDna is None:
            self.generateDna()
        else:
            self.replicateDna(parentDna)
        # self.printGenes('Instantiate')

    # generate DNA which totals to 100
    # each gene is a fractionof this 100
    def generateDna(self):
        hopDistance = random.randint(MIN_GENE, MAX_GENE)
        smell = random.randint(MIN_GENE, MAX_GENE)
        stamina = random.randint(MIN_GENE, MAX_GENE)
        poison = random.randint(MIN_GENE, MAX_GENE)
        normalise = 100 / (hopDistance + smell + stamina + poison)
        self.hopDistance = hopDistance * normalise
        self.smell = smell * normalise
        self.stamina = stamina * normalise
        self.poison = poison * normalise

    # Add fuzz to each parent gene, then normalise back so that total is still 100
    def replicateDna(self, parentDna):
        hopDistance = parentDna.hopDistance + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        smell = parentDna.smell + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        stamina = parentDna.stamina + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        poison = parentDna.poison + random.randint(-GENE_REPLICATION_FUZZ, GENE_REPLICATION_FUZZ)
        if hopDistance < 0:
            hopDistance = 0
        if smell < 0:
            smell = 0
        if stamina < 0:
            stamina = 0
        if poison < 0:
            poison = 0
        normalise = 100 / (hopDistance + smell + stamina + poison)
        self.hopDistance = hopDistance * normalise
        self.smell = smell * normalise
        self.stamina = stamina * normalise
        self.poison = poison * normalise

    def printGenes(self, message, id):
        print(message + 'id={} ho={} st={} sm={} poi={}'.format(id, self.hopDistance, self.stamina, self.smell, self.poison))

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
        # This varies [0,1] for [poor, good]
        normalisedStamina = ((stamina - NORMALISED_GENE_MIN) / NORMALISED_GENE_RANGE) 
        # If factor is 0.6, then foodCostFactor = [1,0] * 0.6 + 0.4 = [1, 0.4] for [poor, good]
        foodCostFactor = (1 - normalisedStamina) * STAMINA_FACTOR + (1 - STAMINA_FACTOR)
        # Weight the food cost by 1 for poor stamina and 0.6 for good stamina (if factor is 0.6)
        self.energy = self.energy - math.sqrt(mx*mx + my*my) * foodCostFactor
        # print('self.energy={} stamina={} correctedStamina={}'.format(self.energy, stamina, foodCostFactor))


# A class to represent a creature 
class Creature:

    serialNumber = 1

    # Constructor to create a new creature
    def __init__(self, screen, parent = None):
        self.screen = screen
        self.id = Creature.serialNumber
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

    def poison(self, poison):
        newenergy = self.energy.energy - poison
        self.energy.energy = newenergy
        print('Poison id={} energy={} poison={}'.format(self.id, self.energy.energy, poison))

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
import math
from constants import *

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

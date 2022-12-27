import random 
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

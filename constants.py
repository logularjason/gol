SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
CREATURE_COUNT=20
FRAMES_PER_SECOND=10 # how fast to run the main loop
CREATURE_STARTING_ENERGY=100 
FOOD_ENERGY=150
FOOD_COUNT=CREATURE_COUNT*4 # number of food
REPLICATION_HEALTH_THRESHOLD = CREATURE_STARTING_ENERGY * 10
ENERGY_SPLITTING_FACTOR=0.5
MAX_GENE=100
MIN_GENE=15
NORMALISED_GENE_MIN=(MIN_GENE)*100/(MIN_GENE+2*MAX_GENE) # the smallest a gene can be after normalised
NORMALISED_GENE_MAX=(MAX_GENE)*100/(2*MIN_GENE+MAX_GENE) # the largest a gene can be after normalised
NORMALISED_GENE_RANGE=NORMALISED_GENE_MAX-NORMALISED_GENE_MIN # the range of normalised gene values
CREATURE_REPLICATION_DISTANCE = 25 # how far away a creature can replicate
GENE_REPLICATION_FUZZ=5 # how much to alter a gene on replication
CREATURE_RADIUS=20
ENERGY_OPACITY_FACTOR=0.1 * 255 / CREATURE_STARTING_ENERGY
STAMINA_FACTOR = 0.3 # food cost will vary on [1-factor, 1] 
POISON_MAX_DISTANCE = 20
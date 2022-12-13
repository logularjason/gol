# Using pygame for graphics.  See this tutorial:
# https://www.pygame.org/docs/ref/draw.html
import pygame as pg
from food import *
from creature import *

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
CREATURE_COUNT=40
FRAMES_PER_SECOND=10 # how fast to run the main loop
CREATURE_STARTING_ENERGY=1000 
FOOD_ENERGY=75
FOOD_CREATURE_FACTOR=1.5 # number of food = number of creatures * FOOD_CREATURE_FACTOR
REPLICATION_HEALTH_THRESHOLD = CREATURE_STARTING_ENERGY * 2
ENERGY_SPLITTING_FACTOR=0.5


# ==========================================
# This function runs the script
# ==========================================
def main():

    # Initialise the pygame framework
    pg.init()

    # Set up the screen
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pg.display.set_caption("Lauras World")

    # Create a list of creatures
    creatureList = CreatureList(screen, SCREEN_WIDTH, SCREEN_HEIGHT, CREATURE_COUNT, CREATURE_STARTING_ENERGY)
    foodlist = Foodlist(screen, creatureList, FOOD_ENERGY, SCREEN_WIDTH, SCREEN_HEIGHT, FOOD_CREATURE_FACTOR)

    # Flag that's used to exit the simulation loop below
    done = False

    # A pygame clock that is used to limit frame rate
    clock = pg.time.Clock()

    while not done:
        # This limits the while loop to a max of n times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(FRAMES_PER_SECOND)

        # Set our done flag if the user closes the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        # Clear the screen before we re-paint the arena
        screen.fill("white")

        # Draw the food
        foodlist.draw()

        # Move the creatures
        creatureList.move(foodlist)

        # Laura TBD: add a replicate method to CreatureList and uncomment the line below to call it 
        # The logic should create another creature with new DNA that is the same as the parent
        creatureList.replicate(REPLICATION_HEALTH_THRESHOLD, ENERGY_SPLITTING_FACTOR)
         

        # Tell pygame to swap its double-buffer (this paints the new frame)
        pg.display.flip()

    # Clean up when our loop completes
    pg.quit()
    quit()

if __name__ == "__main__":
    main()
# Using pygame for graphics.  See this tutorial:
# https://www.pygame.org/docs/ref/draw.html
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from food import *
from creature import *
from constants import *

# ==========================================
# This function runs the script
# ==========================================
def main():

    # Initialise the pygame framework
    pg.init()

    # Set up the screen
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], 0, 32)
    pg.display.set_caption("Lauras Game of Life")

    # Create a list of creatures
    creatureList = CreatureList(screen)
    foodlist = Foodlist(screen, creatureList)

    # Flag that's used to exit the simulation loop below
    done = False

    # A pygame clock that is used to limit frame rate
    clock = pg.time.Clock()

    # A few helpers for plotting a histogram
    i = 0
    bins = range(0,101,2)

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
        creatureList.replicate()
         
        # Tell pygame to swap its double-buffer (this paints the new frame)
        pg.display.flip()

        i = i + 1
        i = i % 20
        if (i is 1):
            histograms = creatureList.dnaHistogram()
            plt.clf()
            plt.hist(histograms[0], bins, alpha=0.5, density=True, edgecolor='black', color='red', label='hop')
            plt.hist(histograms[1], bins, alpha=0.5, density=True, edgecolor='black', color='green', label='smell')
            plt.hist(histograms[2], bins, alpha=0.5, density=True, edgecolor='black', color='blue', label='stamina')
            plt.legend(loc='upper right')
            plt.pause(0.05)


    # Clean up when our loop completes
    pg.quit()
    quit()

if __name__ == "__main__":
    main()
#IMPORTS
import pygame as pg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#CONSTANTS
SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
CANDIDATE_RADIUS=15
FRAMES_PER_SECOND=10
CANDIDATE_COUNT=10



class Candidate:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.draw("white")

    def draw(self, colour):
        self.colour = "white"
        self.borderColour = "black"
        radius = CANDIDATE_RADIUS
        surface1 = pg.Surface((radius*2, radius*2))
        #surface1.set_colorkey("black")
        pg.draw.circle(surface1, colour, [radius, radius], radius)
        print("x is: ", self.x)
        self.screen.blit(surface1, [self.x-radius, self.y-radius])


# A class to represent a list of candidates
class CandidateList:

    # Constructor to create a new candidate
    def __init__(self, screen):
        self.screen = screen
        self.candidate = []
        # Repeatedly create candidates
        for c in range(CANDIDATE_COUNT):
            x = 20 * c
            y = 400
            self.candidate = self.candidate + [Candidate(screen, x, y)]



def main():

    # Initialise the pygame framework
    pg.init()
    clock = pg.time.Clock()
    # Set up the screen
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], 0, 32)
    pg.display.set_caption("THE DATING GAME")
    done = False
    
    while not done:
        # This limits the while loop to a max of n times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(FRAMES_PER_SECOND)

        screen.fill("white")
        candidateList = CandidateList(screen)

        # Tell pygame to swap its double-buffer (this paints the new frame)
        pg.display.flip()

        # Set our done flag if the user closes the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                

if __name__ == "__main__":
    main()

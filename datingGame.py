#IMPORTS
import pygame as pg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random 

#CONSTANTS
SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
CANDIDATE_RADIUS=15
FRAMES_PER_SECOND=10
CANDIDATE_COUNT=10
SAMPLE_SIZE = 3
#font = pg.font.Font(None, 32)
pg.font.init()
font = pg.font.SysFont("comicsansms", 12)



class Candidate:
    def __init__(self, screen, id):
        self.screen = screen
        self.id = id

    def draw(self, colour, x, y):
        radius = CANDIDATE_RADIUS
        surface1 = pg.Surface((radius*2, radius*2))
        surface1.fill('white')
        convertedId = str(self.id)
        #surface1.set_colorkey("black")
        pg.draw.circle(surface1, colour, [radius, radius], radius)
        #print("x is: ", self.x)
        self.screen.blit(surface1, [x-radius, y-radius])
        text = font.render(convertedId, True, "white")
        self.screen.blit(text, [x-radius*0.6, y-radius*0.6])
       


# A class to represent a list of candidates
class CandidateList:

    # Constructor to create a new candidate
    def __init__(self, screen):
        self.screen = screen
        self.candidate = []
        # Repeatedly create candidates
        for cand in range(CANDIDATE_COUNT):
            self.candidate = self.candidate + [Candidate(screen, cand)]

    def bestSample(self):
        bcid = float(CANDIDATE_COUNT + 1)
        sampleCandidates = self.candidate[0:SAMPLE_SIZE]
        for candidate in sampleCandidates:
            d = candidate.id
            if (d < bcid):
                bcid = d
        return bcid

    def bestAS(self):
        #AS stands for after sample 
        bestId = self.bestSample()
        AScandidates = self.candidate[SAMPLE_SIZE:CANDIDATE_COUNT]
        for candidate in AScandidates:
            e = candidate.id
            if (e < bestId):
                bestId = e
                if e > bestId:
                    bestId = self.candidate(CANDIDATE_COUNT)
        return bestId
  
    def findCandidate(self, idToFind):
        for c in self.candidate:
            if c.id == idToFind:
                return c

    def draw(self):
        y = 400
        x = 80
        for cand in self.candidate[0:SAMPLE_SIZE]:
            cand.draw("blue", x, y)
            x = x + 55
        for cand in self.candidate[SAMPLE_SIZE:CANDIDATE_COUNT]:
            cand.draw("red", x, y)
            x = x + 55
        bestCandidateId = self.bestAS()
        bestCandidate = self.findCandidate(bestCandidateId)
        bestCandidate.draw("green", x, y)


   
def main():

    # Initialise the pygame framework
    pg.init()
    clock = pg.time.Clock()
    # Set up the screen
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], 0, 32)
    pg.display.set_caption("THE DATING GAME")
    done = False

    candidateList = CandidateList(screen)
    random.shuffle(candidateList.candidate)
    
    while not done:
        # This limits the while loop to a max of n times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(FRAMES_PER_SECOND)

        screen.fill("white")
        candidateList.draw()

        # Tell pygame to swap its double-buffer (this paints the new frame)
        pg.display.flip()

        # Set our done flag if the user closes the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                

if __name__ == "__main__":
    main()

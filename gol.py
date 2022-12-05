# The tkinter library allows us to use the screen
# This library is described here: https://docs.python.org/3/library/tk.html
import tkinter as tk
import time
import random 
import math


# A class to model the traits of a creature
class DNA:

    # Create new DNA.  We use the parent DNA if it is passed to the constructor
    # Note that parentDna has a default of None if no argument is passed
    def __init__(self, parentDna = None):
        if parentDna is None:
            self.hopDistance = random.randint(1, 20)
        else:
            self.hopDistance = parentDna.hopDistance # Use the parent's DNA

# Hold the energy of a creature and provide methods to calculate
# changes to energy based on movement, etc.
class Energy:

    # Create new DNA
    def __init__(self):
        self.energy = 100

    # Update our health based on move distance - moving has a cost
    def updateEnergy(self, mx, my):
        self.energy = self.energy - math.sqrt(mx*mx + my*my)


# A class to represent a creature 
class Creature:

    # Constructor to create a new creature
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)
        self.dna = DNA()
        self.energy = Energy()
        self.creature = canvas.create_oval(self.x , self.y, self.x+10, self.y+10, outline='red')
   
    # Calculate our move vector based on our hopDistance
    def calculateMoveVector(self):
        self.mx = random.randint(-5, 5) * self.dna.hopDistance
        self.my = random.randint(-5, 5) * self.dna.hopDistance
        # Do not let the creature move out of bounds
        if (self.mx > 999):
            mx = 999
        if (self.mx < 1):
            self.mx = 1
        if (self.my > 999):
            self.my = 999
        if (self.my < 1):
            self.my = 1

    # Clean up when we die
    def die(self):
        self.canvas.delete(self.creature)

    # Move and die if no energy left
    def move(self):
        self.calculateMoveVector()
        self.energy.updateEnergy(self.mx, self.my)
        # Move if we have enerty or die
        if self.energy.energy > 0:
            self.canvas.move(self.creature, self.mx, self.my)
            self.x = self.x + self.mx
            self.y = self.y + self.my
            return True
        else:
            self.die()
            return False

    

# A function containing the initialisation logic
# We put this into a function to keep the code tidy
def createCanvas(window):
    # Make the root window only have on column and row for placing child widgets
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    # Create a canvas
    canvas = tk.Canvas(window, width=1000, height=1000)
    # Place the canvas widget within the root window at row=0 and col=0
    canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    # Draw a border around the canvas
    # Creating items in tkinter is described here: https://tkdocs.com/tutorial/canvas.html#creating
    canvas.create_rectangle(1, 1, 1000, 1000, outline='red')
    return canvas

# Create a list of creatures
def createCreatures(canvas, creatureCount):
    # This is a local variable containing an empty list
    # Read up on lists and tuples; e.g. https://realpython.com/python-lists-tuples/
    creatures = []
    # Repeatedly create creatures
    # Each creature is created with a different location and appended to our list
    # See how it's possible to use '+' to append lists?
    for c in range(creatureCount):
        creatures = creatures + [Creature(canvas)]
    # Return the list to the caller
    return creatures

# A function to move the list of creatures
def moveCreatures(window, canvas, creatures):
    movementCount = 50
    # Move the creatures repeatedly
    while movementCount > 0:
        # Move each creature
        for creature in creatures:
            didMove = creature.move()
            if didMove is False:
                creatures.remove(creature)
        # Decrease counter and sleep
        window.update()
        movementCount = movementCount - 1
        time.sleep(0.1)

# ==========================================
# The script starts executing below
# ==========================================
window = tk.Tk()
canvas = createCanvas(window)

# Create a list of creatures
# LAURA: see if you can figure out how to give each creature a random starting location on the screen
# Clue: read up on the function random() and use it for the x and y starting location
creatures = createCreatures(canvas, 10)

# Move the creatures
moveCreatures(window, canvas, creatures)
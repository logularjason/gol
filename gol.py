# The tkinter library allows us to use the screen
# This library is described here: https://docs.python.org/3/library/tk.html
import tkinter as tk
import time

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
    creatures = []
    # Repeatedly create creatures
    for c in range(creatureCount):
        # Each creature is created with a different location and appended to our list
        creatures = creatures + [canvas.create_oval(c * 15 + 10 , 10, c * 15 + 20, 20, outline='red')]
    # Return the list to the caller
    return creatures

# A function to move the list of creatures
def moveCreatures(window, canvas, creatures):
    movementCount = 20
    x, y = 5, 5
    # Move the creatures repeatedly
    while movementCount > 0:
        # Move each creature
        for creature in creatures:
            canvas.move(creature, x, y)
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
creatures = createCreatures(canvas, 10)

# Move the creatures
moveCreatures(window, canvas, creatures)
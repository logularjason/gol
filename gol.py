# The tkinter library allows us to use the screen
# This library is described here: https://docs.python.org/3/library/tk.html
import tkinter as tk
import time

# A function to move a creature
def moveCreature(window, canvas, creature):
    iterations = 20
    x, y = 5, 5
    while iterations > 0:
        canvas.move(creature, x, y)
        window.update()
        iterations = iterations - 1
        time.sleep(0.1)

# ==========================================
# The script starts executing below
# ==========================================

rootWindow = tk.Tk()
# Make the root window only have on column and row for placing child widgets
rootWindow.columnconfigure(0, weight=1)
rootWindow.rowconfigure(0, weight=1)
# Create a canvas
canvas = tk.Canvas(rootWindow, width=1000, height=1000)
# Place the canvas widget within the root window at row=0 and col=0
canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
# Draw a border around the canvas
# Creating items in tkinter is described here: https://tkdocs.com/tutorial/canvas.html#creating
canvas.create_rectangle(1, 1, 1000, 1000, outline='red')

# Create a creature
creature = canvas.create_oval(10, 10, 20, 20, outline='red')

# Run the simulation
moveCreature(rootWindow, canvas, creature)
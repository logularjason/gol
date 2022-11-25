# These two libraries allow us to use the screen
# This library is described here: https://docs.python.org/3/library/tk.html
# More info here: https://tkdocs.com/tutorial/index.html
from tkinter import *
from tkinter import ttk

# A function to save the position in the event parameter to global variables
def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

# A function to draw a line from the last position to the current
# position (which is carried in the event parameter)
def addLine(event):
    canvas.create_line((lastx, lasty, event.x, event.y))
    savePosn(event)

# ==========================================
# The script starts executing below
# ==========================================

# Initialise the tk library
rootWindow = Tk()
# Make the root window only have on column and row for placing child widgets
rootWindow.columnconfigure(0, weight=1)
rootWindow.rowconfigure(0, weight=1)

# Create a canvas
canvas = Canvas(rootWindow, width=1000, height=1000)

# Place the canvas widget within the root window at row=0 and col=0
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

# Tell the canvas that button presses and mouse motion will be handled by our functions
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", addLine)

# Draw a border around the canvas
# Creating items in tkinter is described here: https://tkdocs.com/tutorial/canvas.html#creating
canvas.create_rectangle(1, 1, 1000, 1000, outline='red')

# Now that we have set up the window, tell it to start processing
rootWindow.mainloop()
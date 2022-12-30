import matplotlib.pyplot as plt
import numpy as np


# ==========================================
# This function runs the script
# ==========================================
def main():
    print(__file__, "has been loaded")

    # Data for plotting
    xAxisValueArray = np.arange(0.0, 2.0, 0.01)
    sinValueArray = 1 + np.sin(2 * np.pi * xAxisValueArray)

    fig, ax = plt.subplots()
    ax.plot(xAxisValueArray, sinValueArray)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("test.png")
    plt.show()


if __name__ == "__main__":
    main()
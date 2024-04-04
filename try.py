import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Creating a new figure and setting up the resolution
fig = plt.figure(dpi=200)

# Change the coordinate system from scalar to polar
ax = fig.add_subplot(projection='polar')

# Generating the X and Y axis data points
r = [8, 8, 8, 8, 8, 8, 8, 8, 8]
theta = np.deg2rad([10, 90, 180, 2, 122, 100, 50, 100, 60])

# Plotting each point separately
for i in range(len(r)):
    ax.plot(theta[i], r[i], marker='o',color="red")

# Setting the axis limit
ax.set_ylim(0, 10)

# Displaying the plot
plt.show()


class Radar():
    fig = plt.figure(dpi=200)
    # Change the coordinate system from scalar to polar
    ax = fig.add_subplot(projection='polar')
    # Generating the X and Y axis data points
    r = [8, 8, 8, 8, 8, 8, 8, 8, 8]
    theta = np.deg2rad([10, 90, 180, 2, 122, 100, 50, 100, 60])

    # Plotting each point separately
    for i in range(len(r)):
        ax.plot(theta[i], r[i], marker='o',color="red")

    # Setting the axis limit
    ax.set_ylim(0, 10)

    # Displaying the plot
    plt.show()
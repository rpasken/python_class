import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


#
# Ask for the name of the file with the data
#

file_name = input("What is the filename for the input data ")

#
# Open and then read the data from the file. Specify that each element is separated
# by a comma
#

geopot = np.loadtxt(file_name, delimiter=",")

#
# Technically I already know how many rows and columns there are in the dataset. The
# next few lines allow me to make the code general and more elegant.
#

num_lats = len(geopot)
num_lons = len(geopot[0])

xm,ym = np.meshgrid(np.arange(num_lons),np.arange(num_lats))

#
# Using the plot library (matplotlib) create a figure, specifically
# 3d projection


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#
# Plot the temperature data on a 3d surface using a specific
# color table and then show the figure
#

ax.plot_surface(xm,ym,geopot,cmap=cm.coolwarm)
plt.show()

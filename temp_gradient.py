import matplotlib.pyplot as plt
import numpy as np
import csv

#
# Ask for the name of the file with the data
#

file_name = input("What is the filename for the input data ")

#
# Open and then read the data from the file. Specify that each element is separa
ted
# by a comma
#

temp = np.loadtxt(file_name, delimiter=",")

#
# Here is a bit of python idiom. Build two 2d lists
# "arrays/matrix" with values from 0 to 12 in x and
# 0 to 8 in y. An equivalent would be
#
# i = np.arange(0,13,1)
#
# make a list of floating point numbers from 0 to 12 counting by 1
# Note that arange is from the numerical python library (numpy)
#
# j = np.arange(0,9,1)
#
# make a list of floating point numbers from 0 to 9 counting by 1
#
# xm,ym = np.meshgrid(i,j)
#
# Create a 2d grid (array/matrix) of values using the i/j values
#

xm,ym = np.meshgrid(np.arange(0,13,1),np.arange(0,9,1))

#
# Using the plot library (matplotlib) create a figure, specifically
# 3d projection


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#
# Plot the temperature data on a 3d surface using a specific
# color table and then show the figure
#

ax.plot_surface(xm,ym,temp,cmap=cm.coolwarm)
plt.show()


#
# Next let's compute the temperature gradient.
#
# First create two empty 2d lists (arrays/matricies), one for the x
# direction and one for y. I just happen to know it is arranged as
# 9 rows and 13 columns
#
dtdx = np.empty((9,13))
dtdy = np.empty((9,13))

#
# This form matches more closely what you would do by hand. You look where
# you are in the grid and choose either a centered or one sided differences
# depending on if you are at a center point or edge point
#
# Walk through all the grid points
#

for y in range(0,9):
    for x in range(0,13):

        #
        # For the x-direction am I at a center point or at the left
        # or right edge.
        #

        if x > 0 and x < 12:            dtdx[y,x] = -(temp[y,x+1] - temp[y,x-1]) / 2
        elif x == 0:
            dtdx[y,x] = -(temp[y,x+1] - temp[y,x]) / 1
        elif x == 12:
            dtdx[y,x] = -(temp[y,x] - temp[y,x-1]) / 1
        #
        # For the y-direction am I at a center point or at the top
        # or bottom edge.
        #

        if y > 0 and y < 8:
            dtdy[y,x] = -(temp[y+1,x] - temp[y-1,x]) / 2
        elif y == 0:
            dtdy[y,x] = -(temp[y+1,x] - temp[y,x]) / 1
        elif y == 9:
            dtdy[y,x] = -(temp[y,x] - temp[y-1,x]) / 1


fig = plt.figure()
ax = fig.add_subplot(111)
ax.quiver(dtdx,dtdy)plt.show()

#
# This method uses the numpy derivative library. Unfortunately it hides
# all the details.
#

dtdx = -np.gradient(temp,axis=1) / 2.0
dtdy = -np.gradient(temp,axis=0) / 2.0

fig = plt.figure()
ax = fig.add_subplot(111)
ax.quiver(dtdx,dtdy)
plt.show()


        


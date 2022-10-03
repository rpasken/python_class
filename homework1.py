import csv
import numpy as np
import matplotlib.pyplot as plt

#
# Get a scan radus and make sure it is a real number
#

scan = float(input("enter a scan radius: "))

#
# Open the file with the data and since it is a comma 
# separated value file use the csv library to read it 
# in
#

datafile = open("xy_locs")
datareader = csv.reader(datafile,delimiter=",")

#
# Make empty lists for the three values to be read in
#

m42> cat homework1.p
cat: homework1.p: No such file or directory
m42> cat homework1.py 
import csv
import numpy as np
import matplotlib.pyplot as plt

#
# Get a scan radus and make sure it is a real number
#

scan = float(input("enter a scan radius: "))

#
# Open the file with the data and since it is a comma 
# separated value file use the csv library to read it 
# in
#

datafile = open("xy_locs")
datareader = csv.reader(datafile,delimiter=",")

#
# Make empty lists for the three values to be read in
#

data= []
lat = []
lon = []

#
# Next define the constants for the program
# In this case fix the size of the domain
#

num_rows = 9
num_columns = 13
delta = 400000.0
f = 1e-04

#
# Create empty lists for the geopotential and vorticity
#

nearest_geopot = np.zeros((num_rows,num_columns))
cressman_geopot = np.zeros((num_rows,num_columns))
vort = np.zeros((num_rows,num_columns))

for item in datareader:
    lon.append(float(item[0]))
    lat.append(float(item[1]))
    data.append(float(item[2]))

for i in range(num_rows):
    for j in range(num_columns):
        dx = float(j)
        dy = float(i)
        total = 0.0
        count = 0
        for k in range(len(data)):
            dist = np.sqrt((dx-lon[k])*(dx-lon[k]) + (dy-lat[k])*(dy-lat[k]))
            if(lon[k]<=dx+scan and lon[k]>=dx-scan and lat[k]<=dy+scan and lat[k]>=dy-scan):
                if dist <= scan:
                    total = total + data[k]
                    count += 1
        nearest_geopot[i][j] = total / count
        
for i in range(num_rows):
    for j in range(num_columns):
        dx = float(j)
        dy = float(i)
        total = 0.0
        total_weight = 0.0
        for k in range(len(data)):
            if(lon[k]<=dx+scan and lon[k]>=dx-scan and lat[k]<=dy+scan and lat[k]>=dy-scan):
                dist = np.sqrt((dx-lon[k])*(dx-lon[k]) + (dy-lat[k])*(dy-lat[k]))
                if dist <= scan:
                    weight = (scan - dist) / (scan+dist)
                    total = total + data[k]*weight
                    total_weight += weight
        cressman_geopot[i][j] = total / total_weight


plt.contour(cressman_geopot,colors="black")
plt.contourf(cressman_geopot-nearest_geopot)
plt.colorbar()
plt.show()

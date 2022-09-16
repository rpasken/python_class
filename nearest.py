import csv
import numpy as np
import matplotlib.pyplot as plt

#
# Define a smoothing function
#

def smooth(factor,array,start_x,end_x,start_y,end_y):
    c = factor
    for i in range(start_x,end_x):
        for j in range(start_y,end_y):
            array[i][j]=array[i][j]+c/4.0*(array[i+1][j]+array[i][j+1]+array[i-1][j]+array[i][j-1]-4.0*array[i][j])
    return array          
    
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
geopot = np.zeros((num_rows,num_columns))
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
            if(lon[k]<=dx+scan and lon[k]>=dx-scan and lat[k]<=dy+scan and lat[k]>=dy-scan):
                total = total + data[k]
                count += 1
        geopot[i][j] = total / count
        


for i in range(1,num_rows-1):
    for j in range(1,num_columns-1):
        vort[i][j]=(geopot[i+1][j]+geopot[i][j+1]+geopot[i-1][j]+geopot[i][j-1]-4.0*geopot[i][j])
        vort[i][j]=vort[i][j]/(delta*delta)
        vort[i][j] = vort[i][j]/f

plt.contour(vort)
c=0.8  
vort = smooth(c,vort,1,num_rows-1,1,num_columns-1)

plt.contour(geopot,colors="black")
plt.contourf(vort)
plt.colorbar()
plt.show()
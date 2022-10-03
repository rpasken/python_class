import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use ("Qt5Agg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#
# Set up some constants for this analysis
#

num_rows = 18
num_cols = 26

f = 1e-04

min_lon = -126.0
max_lon = -62.0
max_lat = 65.0
min_lat = 23.0
cen_lon = -100.0
cen_lat = 40.0

#
# Open the plot and setup the map projection info
#

fig = plt.figure()
proj = ccrs.LambertConformal(central_longitude=cen_lon, central_latitude=cen_lat)
ax = fig.add_subplot(1, 1, 1, projection=proj)

#
# Next set the areal extent of the map to cover most of the CONUS
#

ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

#
# Let's add some features to the map
#

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.STATES)
#
# Next build the grid, by dividing the latitude and longitude extremes by
# the number of grid squares
#

lat_step = (max_lat - min_lat)  / num_rows
lon_step = (max_lon - min_lon) / num_cols

#
# Assume that 1 deg lat/lon is 110km
#

delta =  lat_step * 110000

#
# Make a mesh from the range of latitudes and longitudes and the step
# size in each direction
#

xm,ym = np.meshgrid(np.arange(min_lon,max_lon,lon_step), np.arange(min_lat,max_lat,lat_step))

#
# Get a scan radus and make sure it is a real number
#

#scan = (lat_step + lon_step) * 3.0
scan = float(input("enter a scan radius: "))
scan = (lat_step + lon_step) * scan
#
# Make empty lists for the three values to be read in
#

data= []
lat = []
lon = []


#
# Open the file with the data and since it is a comma 
# separated value file use the csv library to read it 
# in
#

datafile = open("/Users/rpasken/courses/2022/fall/comp_tech/python/ualatlon")
datareader = csv.reader(datafile,delimiter=",")

for item in datareader:
    lon.append(-float(item[3]))
    lat.append(float(item[2]))
    data.append(float(item[5]))


datafile.close()

geopot = np.zeros((num_rows,num_cols))

ucomp = np.zeros((num_rows,num_cols))
vcomp =np.zeros((num_rows,num_cols))
vort = np.zeros((num_rows,num_cols))

analysis(scan,num_rows,num_cols,xm,ym,data,cressman_geopot)

for i in range(num_rows):
    for j in range(num_cols):
        vcomp[i,j]  = 1/f * ddx(geopot,i,j,delta)
        ucomp[i,j]  = -1/f * ddy(geopot,i,j,delta)

for i in range(num_rows): 
    for j in range(num_cols):
        vort[i,j] = ddx(vcomp,i,j,delta) + ddy(ucomp,i,j,delta)

for i in range(num_rows):
    for j in range(num_cols):
        vort_advec[i,j] = ucomp[i,j] * ddx(vcomp,i,j,delta) + vcomp[i,j] * ddy(ucomp,i,j,delta)
"""
for i in range(len(lat)):     
    plt.text(lon[i],lat[i],"+",transform=ccrs.PlateCarree())
"""  
plt.contour(xm,ym,geopot,colors="black",transform=ccrs.PlateCarree())
#plt.contourf(xm,ym,cressman_geopot-nearest_geopot,transform=ccrs.PlateCarree())
#plt.colorbar()
plt.contourf(xm,ym,vort,transform=ccrs.PlateCarree())
#plt.contourf(xm,ym,vort_advec,transform=ccrs.PlateCarree())
#plt.quiver(xm,ym,ucomp,vcomp,transform=ccrs.PlateCarree())
plt.colorbar()
plt.show()


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from metpy.units import units
from metpy.interpolate import interpolate_to_grid
from metpy.plots import StationPlot

to_proj = ccrs.LambertConformal(central_longitude=-100, central_latitude=40.)


#data = pd.read_csv('./wthr_202210302050.qct',delim_whitespace=True)

data = pd.read_csv('./wthr_202211071955.qc',delim_whitespace=True ,header=0, usecols=(0, 1, 2, 4, 6, 8, 10, 12, 14, 16),
                      names=['id','lat', 'lon','tmpf', 'relh','mslp','uwind','vwind','gust','precip'])
data = data[['id','lat','lon','tmpf','relh','mslp','uwind','vwind','gust']]

locs = pd.read_csv('./seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])
locs = locs[['name','call_sign']]

new_data = pd.merge(data,locs,left_on='id',right_on='call_sign')
temp = new_data = new_data.drop('call_sign',axis=1)


temperature = new_data['tmpf'].values * units.degF
humid = new_data['relh']
pressure = new_data['mslp'].values * units.hPa
u = new_data['uwind'].values * units.mph
v = new_data['vwind'].values * units.mph
gust = new_data['gust'].values * units.mph

lat = new_data['lat'].values
lon = new_data['lon'].values
station_id = new_data['id']
cloud = np.zeros(len(lon)).astype(int)

xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T

slpgridx, slpgridy, slp = interpolate_to_grid(xp, yp, pressure,
                                              interp_type='barnes', minimum_neighbors=3,
                                              search_radius=50000, hres=10000)

#x_masked, y_masked, t = remove_nan_observations(xp, yp, data['tmpf'].values)
tempx, tempy, temp = interpolate_to_grid(xp, yp, temperature, interp_type='barnes',
                                         minimum_neighbors=3, search_radius=50000, hres=10000)



levels = list(np.arange(np.min(new_data['tmpf']), np.max(new_data['tmpf']),1))
cmap = plt.get_cmap('coolwarm')




fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=to_proj)
#ax.set_extent([-92, -89, 38, 39.5])

ax.set_extent([-95.3, -89.2, 36, 40.5])

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
mmb = ax.contourf(tempx, tempy, temp, cmap=cmap)
fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)
"""
for i in range(len(new_data['lon'])):
    plt.text(xp[i],yp[i],new_data['name'][i],fontsize=8) 

"""
plt.show()
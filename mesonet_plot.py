#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:34:39 2022

@author: rpasken
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metpy.interpolate import interpolate_to_grid
import metpy.calc as mpc
from metpy.plots import StationPlot
from metpy.units import units

to_proj = ccrs.LambertConformal(central_longitude=-94., central_latitude=38.)


data = pd.read_csv('/eas/ap/rpasken/wthr_202211050730.qc',delim_whitespace=True ,header=0, usecols=(0, 1, 2, 4, 6, 8, 10, 12, 14, 16),
                      names=['stn','lat', 'lon','tmpf', 'relh','mslp','uwind','vwind','gust','precip'])


locs = pd.read_csv('/eas/ap/rpasken/seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])
meso_locs = pd.read_csv('/eas/ap/rpasken/seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])
locs = locs[['name','call_sign']]

new_data = pd.merge(data,locs,left_on='stn',right_on='call_sign')

new_data = new_data.drop('call_sign',axis=1)
print(new_data.head())

temperature = new_data['tmpf'].values * units.degF
humid = new_data['relh']
pressure = new_data['mslp'].values * units.hPa
u = new_data['uwind'].values * units.mph
v = new_data['vwind'].values * units.mph
gust = new_data['gust'].values * units.mph
lat = new_data['lat'].values
lon = new_data['lon'].values
station_id = new_data['stn']
cloud = np.zeros(len(lon)).astype(int)

xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(),lon,lat).T


slpgridx, slpgridy, slp = interpolate_to_grid(xp, yp, pressure,
                                              interp_type='cressman', minimum_neighbors=1,
                                              search_radius=60000, hres=15000)


tempx, tempy, temp = interpolate_to_grid(xp, yp, temperature, interp_type='cressman',
                                         minimum_neighbors=1, search_radius=60000, hres=15000)



levels = list(np.arange(np.min(new_data['tmpf']), np.max(new_data['tmpf']),1))
cmap = plt.get_cmap('coolwarm')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig = plt.figure(figsize=(20, 10))
view = fig.add_subplot(1, 1, 1, projection=to_proj)
#view.set_extent([-92, -89, 38, 40])

view.set_extent([-96, -89, 36, 41])

view.add_feature(cfeature.STATES.with_scale('50m'))
view.add_feature(cfeature.OCEAN)
view.add_feature(cfeature.COASTLINE.with_scale('50m'))
view.add_feature(cfeature.BORDERS, linestyle=':')

cs = view.contour(slpgridx, slpgridy, slp, colors='k', levels=list(range(990, 1034, 1)))
view.clabel(cs, inline=1, fontsize=8, fmt='%i')

mmb = view.contourf(tempx, tempy, temp, cmap=cmap, norm=norm)
fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)

for i in range(len(new_data['lon'])):
    plt.text(meso_locs['lon'][i],meso_locs['lat'][i],meso_locs['name'][i],transform=ccrs.PlateCarree())    
"""
stationplot = StationPlot(view, lon, lat, clip_on=True,
                          transform=ccrs.PlateCarree(), fontsize=8)
# Plot the temperature and dew point to the upper and lower left, respectively, of
# the center point. Each one uses a different color.
stationplot.plot_parameter('NW', temperature, color='red')
stationplot.plot_parameter('SW', humid, color='darkgreen')
stationplot.plot_parameter('E', gust, color='darkgreen')
stationplot.plot_parameter('NE', pressure, formatter=lambda v: format(10 * v, '.0f')[-3:])
stationplot.plot_parameter('C',cloud,color='black')
# Add wind barbs
stationplot.plot_barb(u, v)

# Also plot the actual text of the station id. Instead of cardinal directions,
# plot further out by specifying a location of 2 incremenwthr_202210241440.qcts in x and -1 in y.
stationplot.plot_text((2, -1), station_id,fontsize=8)
view.set_title('Surface Temperature (shaded) and SLP.')
"""
plt.show()


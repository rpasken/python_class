import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metpy.interpolate import interpolate_to_grid, remove_nan_observations

from metpy.plots import StationPlot
from metpy.units import units

to_proj = ccrs.LambertConformal(central_longitude=-94., central_latitude=38.)

#data = pd.read_csv('/eas/ap/rpasken/dum.csv', na_values=' ')
data = pd.read_csv('/eas/ap/rpasken/wthr_202210211725.csv',header=0, usecols=(0, 1, 2, 4, 6, 8, 10, 12, 14, 16),
                      names=['stn','lat', 'lon', 'tmpf', 'relh','mslp', 'uwind','vwind','gust','precip'])
temperature = data['tmpf'].values * units.degF
humid = data['relh']
pressure = data['mslp'].values * units.hPa
u = data['uwind'].values * units.mph
v = data['vwind'].values * units.mph
gust = data['gust'].values * units.mph
lat = data['lat'].values
lon = data['lon'].values
station_id = data['stn']
cloud = np.zeros(len(lon)).astype(int)

xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T
x_masked, y_masked, pressure = remove_nan_observations(xp, yp, data['mslp'].values)
slpgridx, slpgridy, slp = interpolate_to_grid(x_masked, y_masked, pressure,
                                              interp_type='barnes', minimum_neighbors=2,
                                              search_radius=50000, hres=5000)

x_masked, y_masked, t = remove_nan_observations(xp, yp, data['tmpf'].values)
tempx, tempy, temp = interpolate_to_grid(x_masked, y_masked, t, interp_type='barnes',
                                         minimum_neighbors=2, search_radius=50000, hres=5000)

temp = np.ma.masked_where(np.isnan(temp), temp)


levels = list(np.arange(np.min(temp), np.max(temp),1))
cmap = plt.get_cmap('viridis')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig = plt.figure(figsize=(20, 10))
view = fig.add_subplot(1, 1, 1, projection=to_proj)
view.set_extent([-92, -89, 38, 40])

#view.set_extent([-96, -89, 36, 41])

view.add_feature(cfeature.STATES.with_scale('50m'))
view.add_feature(cfeature.OCEAN)
view.add_feature(cfeature.COASTLINE.with_scale('50m'))
view.add_feature(cfeature.BORDERS, linestyle=':')

cs = view.contour(slpgridx, slpgridy, slp, colors='k', levels=list(range(990, 1034, 4)))
view.clabel(cs, inline=1, fontsize=12, fmt='%i')

mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)

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
# plot further out by specifying a location of 2 increments in x and -1 in y.
stationplot.plot_text((2, -1), station_id,fontsize=8)
view.set_title('Surface Temperature (shaded) and SLP.')

plt.show()

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, StationPlot
from metpy.units import units

data = pd.read_csv('/home/rpasken/Desktop/dum.csv', na_values=' ')

proj = ccrs.LambertConformal(central_longitude=-98)
point_locs = proj.transform_points(ccrs.PlateCarree(), data['lon'].values, data['lat'].values)
data = data[mpcalc.reduce_point_density(point_locs, 50 * units.km)]


temperature = data['tmpf'].values * units.degF
humid = data['relh']
pressure = data['mslp'].values * units.hPa
u = data['uwind'].values * units.mph
v = data['vwind']
gust = data['gust']
latitude = data['lat']
longitude = data['lon']
station_id = data['stn']
print(len(station_id))

# Create the figure and an axes set to the projection.
fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(1, 1, 1, projection=proj)

# Add some various map elements to the plot to make it recognizable.
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.STATES.with_scale('50m'))

# Set plot bounds
ax.set_extent([-95, -89, 36, 41])


stationplot = StationPlot(ax, longitude.values, latitude.values, clip_on=True,
                          transform=ccrs.PlateCarree(), fontsize=12)

# Plot the temperature and dew point to the upper and lower left, respectively, of
# the center point. Each one uses a different color.
stationplot.plot_parameter('NW', temperature, color='red')
stationplot.plot_parameter('SW', humid, color='darkgreen')
stationplot.plot_parameter('E', gust, color='darkgreen')

# A more complex example uses a custom formatter to control how the sea-level pressure
# values are plotted. This uses the standard trailing 3-digits of the pressure value
# in tenths of millibars.
stationplot.plot_parameter('NE', pressure.m, formatter=lambda v: format(10 * v, '.0f')[-3:])

# Add wind barbs
stationplot.plot_barb(u, v)

# Also plot the actual text of the station id. Instead of cardinal directions,
# plot further out by specifying a location of 2 increments in x and -1 in y.
stationplot.plot_text((2, -1), station_id,fontsize=8)

# Add title and display figure
plt.title('SEAMLESS Mesonet Observations', fontsize=10, loc='left')
plt.title('Time: 18:25 UTC 17 October 2022', fontsize=10, loc='right')
plt.show()
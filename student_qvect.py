import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt

from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metpy.interpolate import interpolate_to_grid
from metpy.units import units
import metpy.calc as mc
from metpy.plots import USCOUNTIES



to_proj = ccrs.LambertConformal(central_longitude=-94., central_latitude=38.)

gridspace = float(input("What is the grid spacing in meters: "))
radius = float(input("What is the scan radius: "))


data = pd.read_csv('/eas/ap/rpasken/wthr_202211111820.qc',delim_whitespace=True ,header=0, usecols=(0, 1, 2, 4, 6, 8, 10, 12, 14, 16),
                      names=['stn','lat', 'lon','tmpf', 'relh','mslp','uwind','vwind','gust','precip'])


locs = pd.read_csv('/eas/ap/rpasken/seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])
meso_locs = pd.read_csv('/eas/ap/rpasken/seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])
locs = locs[['name','call_sign']]

new_data = pd.merge(data,locs,left_on='stn',right_on='call_sign')

new_data = new_data.drop('call_sign',axis=1)

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


slpgridx, slpgridy, slp = interpolate_to_grid(xp, yp, pressure,interp_type='cressman', 
                                              minimum_neighbors=1,search_radius=radius, 
                                              hres=gridspace)


tempx, tempy, temp = interpolate_to_grid(xp, yp, temperature, interp_type='cressman',
                                         minimum_neighbors=1, search_radius=radius, 
                                         hres=gridspace)

ux, uy, uwind = interpolate_to_grid(xp, yp, u, interp_type='cressman',
                                         minimum_neighbors=1, search_radius=radius, 
                                         hres=gridspace)

vx, vy, vwind = interpolate_to_grid(xp, yp, v, interp_type='cressman',
                                         minimum_neighbors=1, search_radius=radius, 
                                         hres=gridspace)

temp = mc.smooth_n_point(temp, 9, 1)
slp = mc.smooth_n_point(slp, 9, 1)

levels = list(np.arange(np.min(new_data['tmpf']), np.max(new_data['tmpf']),1))
cmap = plt.get_cmap('coolwarm')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig = plt.figure(figsize=(20, 10))
view = fig.add_subplot(1, 1, 1, projection=to_proj)

#view.set_extent([-92, -89, 38, 40])

view.set_extent([-95.6, -90.0, 36, 40.5])


view.add_feature(cfeature.STATES.with_scale('50m'))
view.add_feature(USCOUNTIES.with_scale('5m'))
view.add_feature(cfeature.OCEAN)
view.add_feature(cfeature.COASTLINE.with_scale('50m'))
view.add_feature(cfeature.BORDERS, linestyle=':')

view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')


#cs = view.contour(slpgridx, slpgridy, slp, colors='k', levels=list(range(990, 1034, 1)))
#view.clabel(cs, inline=1, fontsize=8, fmt='%i')

mmb = view.contourf(tempx, tempy, temp, cmap=cmap, norm=norm)
fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)

view.set_title('Surface Temperature (shaded) and SLP.')

plt.show()

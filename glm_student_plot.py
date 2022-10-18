#!/usr/bin/env python3
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from goes2go.data import goes_latest

g16_glm = goes_latest(satellite='G16', product='GLM')
g16_abi = goes_latest(satellite='G16', product='ABI')

project = g16_abi.rgb.crs

#g17 = goes_latest(satellite='G17', product='GLM')

event_lat = g16_glm.variables['event_lat'][:]
event_lon = g16_glm.variables['event_lon'][:]
flash_lat = g16_glm.variables['flash_lat'][:]
flash_lon = g16_glm.variables['flash_lon'][:]

fig = plt.figure(figsize=(8, 6))

#
# Create axis with Geostationary projection
#

ax = plt.axes(projection=project)

#ax.set_extent([-95, -89, 36, 41])
ax.set_extent([-120, -70, 20, 56])


ax.coastlines(resolution='50m', color='red')

ax.imshow(g16_abi.rgb.NaturalColor(), **g16_abi.rgb.imshow_kwargs)


plt.show()

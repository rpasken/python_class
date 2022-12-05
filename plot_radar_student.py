import cartopy
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import os
import io
import glob

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from metpy.io import Level2File
from metpy.plots import ctables, add_timestamp
from metpy.plots import USCOUNTIES
from matplotlib.animation import ArtistAnimation


#
# Open the NEXRAD data file
#


radar = "KLSX"
field = ['Reflectivity']
dir = "./radar/" + radar + "/" + date + "/" + hour + '/'
        
filelist = os.listdir(dir)
filelist = sorted(filelist)

artists = []

g = Level2File(dir + "/" + filelist[0])
  
# 
# Pull data out from the file
#

rLAT = g.sweeps[0][0][1].lat
rLON = g.sweeps[0][0][1].lon
center_pt = [rLAT,rLON]
extent = [center_pt[1]-1.0,center_pt[1]+1.0,center_pt[0]-1.0,center_pt[0]+1.0]
proj = cartopy.crs.LambertConformal(central_longitude=rLON, central_latitude=rLAT)


fig = plt.figure(figsize=(10,8))
view = fig.add_subplot(1,1,1,projection=proj)

for file in filelist:    
    
    f = Level2File(dir + "/" + file)

    print(str(f.dt))
    # 
    # First item in ray is header, which has azimuth angle
    #

    sweep = 0
    az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
    diff = np.diff(az)
    diff[diff > 180] -= 360.
    diff[diff < -180] += 360.
    avg_spacing = diff.mean()
    az = (az[:-1] + az[1:]) / 2
    az = np.concatenate(([az[0] - avg_spacing], az, [az[-1] + avg_spacing]))

    #
    # 5th item is a dict mapping a var name (byte string) to a tuple
    # of (header, data array)
    #
    # Refelctivity data is available for all sweeps
    #

    refl_sweep = 0
    
    ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
    ref_range = (np.arange(ref_hdr.num_gates+1) - 0.5) * ref_hdr.gate_width + ref_hdr.first_gate
    ref = (np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]]))

       
    xlocs = ref_range * np.sin(np.deg2rad(az[:, np.newaxis]))
    ylocs = ref_range * np.cos(np.deg2rad(az[:, np.newaxis]))
    lon = rLON + xlocs/110
    lat = rLAT + ylocs/110
    
    view.set_aspect('equal', 'datalim')
    view.set_extent(extent)


    #
    # Plot the data
    #
    
    color_map = ctables.registry.get_colortable('Carbone42')
    min = 5
    max = 55
    type = 'REF'
    cb = view.pcolormesh(lon,lat,ref,vmin=min,vmax=max,cmap=color_map,transform=ccrs.PlateCarree())
    text = view.text(0.5,1.02,radar + " " + str(f.dt),ha="center",transform=view.transAxes)
    artists.append((text,cb))


anim = ArtistAnimation(fig,artists,interval=100,blit=True,repeat_delay=1000)
plt.show()

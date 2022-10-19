
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("Qt5agg")

from metpy.cbook import get_test_data
from metpy.io import Level2File
from metpy.plots import  add_timestamp, ctables

# 
# Open the NEXRAD data file
#

name = get_test_data('KTLX20130520_201643_V06.gz', as_file_obj=False)
f = Level2File('KLSX20220726_174630_V06')

# 
# Pull data out for the first sweep from the file
#

sweep = 0

# 
# First item in ray is header, which has azimuth angle
#

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

ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
ref_range = (np.arange(ref_hdr.num_gates + 1) - 0.5) * ref_hdr.gate_width + ref_hdr.first_gate
ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

var_data = ref
var_range = ref_range

# 
# Turn into an array, then mask
#

data = np.ma.array(var_data)
data[np.isnan(data)] = np.ma.masked

# 
# Convert az,range to x,y
#

xlocs = var_range * np.sin(np.deg2rad(az[:, np.newaxis]))
ylocs = var_range * np.cos(np.deg2rad(az[:, np.newaxis]))

# 
# Plot the data
#

ax.pcolormesh(xlocs, ylocs, data)
ax.set_aspect('equal', 'datalim')
ax.set_xlim(-40, 20)
ax.set_ylim(-30, 30)
add_timestamp(ax, f.dt, y=0.02, high_contrast=True)

plt.show()
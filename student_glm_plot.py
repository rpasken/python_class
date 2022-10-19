
from goes2go.data import goes_latest, goes_nearesttime
from goes2go.rgb import normalize, TrueColor, NaturalColor
from goes2go.tools import abi_crs
import matplotlib.pyplot as plt

#
# get latest data
#

g_abi = goes_latest(satellite='G16', product='ABI', domain='C')

ax = plt.subplot(projection=g_abi.rgb.crs)

ax.imshow(g_abi.rgb.NaturalColor(), **g_abi.rgb.imshow_kwargs)

plt.show()
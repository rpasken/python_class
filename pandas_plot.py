
import cartopy.crs as ccrs
import pandas as pd


to_proj = ccrs.LambertConformal(central_longitude=-94., central_latitude=38.)


data = pd.read_csv('/eas/ap/rpasken/wthr_202210241440.qc',delim_whitespace=True ,header=0, usecols=(0, 1, 2, 4, 6, 8, 10, 12, 14, 16),
                      names=['stn','lat', 'lon','tmpf', 'relh','mslp','uwind','vwind','gust','precip'])
data = data[['stn','lat','lon','tmpf','relh','mslp','uwind','vwind','gust']]
print(data.head())
locs = pd.read_csv('/eas/ap/rpasken/seamless_stations',header=0,names=['meso_id','call_sign','name','lat', 'lon','altitude'])

locs = locs[['name','call_sign']]

new_data = pd.merge(data,locs,left_on='stn',right_on='call_sign')

temp = new_data = new_data.drop('call_sign',axis=1)

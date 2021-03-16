import xarray as xr
import pyproj
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pandas import DataFrame
import pyproj
from datetime import date, datetime, timedelta 
#from os import path
import config

engine = create_engine("mysql+pymysql://{user}:{pw}@{srv}/{db}"
                       .format(user=config.sqluser,
                              pw=config.sqlpwd,
                              srv=config.sqlserver,
                              db=config.sqldb))

df_roads = pd.read_sql_table(
    "road_information",
    con=engine
)

try:
    df_maxDate = pd.read_sql_query("SELECT max(forecast_ref_time) maxdate FROM historic_weather_predictions", con=engine)
    dt = pd.to_datetime(df_maxDate['maxdate'][0]).to_pydatetime().date() + timedelta(days=1)
except:
    dt = date(2015,1,1)

dtend = date.today()

while dt < dtend:

    if dt < date(2019, 11, 26):
        baseurl = 'https://thredds.met.no/thredds/dodsC/metpparchivev1/'
    else:
        baseurl = 'https://thredds.met.no/thredds/dodsC/metpparchive/'

    if dt.month in {10,11,12,1,2,3,4,5}:  # tar kun med vintermåneder

        fullurl = baseurl \
            + str(dt.year) + '/' \
            + str(dt.month).zfill(2) + '/' \
            + str(dt.day).zfill(2) + '/' \
            + 'met_forecast_1_0km_nordic_' \
            + str(dt.year) \
            + str(dt.month).zfill(2) \
            + str(dt.day).zfill(2) \
            + 'T06Z.nc'

        try:
            file = xr.open_dataset(fullurl)

            for index, row in df_roads.iterrows():
                proj = pyproj.Proj(file.projection_lcc.proj4)
                X,Y = proj(row['longitude'],row['latitude'])

                df = DataFrame()
                for c in range(6, 59, 6):
                    df = df.append({"station_id": row['station_id']
                        , "forecast_ref_time": file.forecast_reference_time.values
                        , "forecast_time": c
                        , "air_temp": file.air_temperature_2m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas() - 273.15
                        , "precipitation_amount": np.float64(file.precipitation_amount.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "wind_bearing": np.float64(file.wind_direction_10m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "wind_speed": np.float64(file.wind_speed_10m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        #, "wind_speed_of_gust": np.float64(file.wind_speed_of_gust.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "cloud_area_fraction": np.float64(file.cloud_area_fraction.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "air_pressure_at_sea_level": np.float64(file.air_pressure_at_sea_level.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "relative_humidity": np.float64(file.relative_humidity_2m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        , "surface_downwelling_shortwave_flux": np.float64(file.integral_of_surface_downwelling_shortwave_flux_in_air_wrt_time.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
                        }, ignore_index=True)
        
                df.to_sql('historic_weather_predictions', con=engine, if_exists='append', index=False)
                
            print(str(dt) + ' - OK')
            
        except:
            print(str(dt) + ' - ERROR')

    dt += timedelta(days=1)


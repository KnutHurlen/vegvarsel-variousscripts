from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pandas import DataFrame
import xarray as xr
import pyproj
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

url = 'https://thredds.met.no/thredds/dodsC/metpplatest/met_forecast_1_0km_nordic_latest.nc'
file = xr.open_dataset(url)

proj = pyproj.Proj(file.projection_lcc.proj4)

engine.execute("TRUNCATE TABLE vegvarsel.weather_predictions")

for index, row in df_roads.iterrows():
    proj = pyproj.Proj(file.projection_lcc.proj4)
    X,Y = proj(row['longitude'],row['latitude'])

    df = DataFrame()
    for c in range(6, 49, 6):
        df = df.append({"road_id": row['road_id']
            , "forecast_ref_time": file.forecast_reference_time.values
            , "time": c
            , "air_temp": file.air_temperature_2m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas() - 273.15
            , "precipitation_amount": np.float64(file.precipitation_amount.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "wind_bearing": np.float64(file.wind_direction_10m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "wind_speed": np.float64(file.wind_speed_10m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "wind_speed_of_gust": np.float64(file.wind_speed_of_gust.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "cloud_area_fraction": np.float64(file.cloud_area_fraction.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "air_pressure_at_sea_level": np.float64(file.air_pressure_at_sea_level.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            , "relative_humidity": np.float64(file.relative_humidity_2m.sel(x=X,y=Y,method="nearest").isel(time=c).to_pandas())
            }, ignore_index=True)
    
    df.to_sql('weather_predictions', con=engine, if_exists='append', index=False)


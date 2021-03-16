from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
from azure.storage.blob import ContainerClient
import numpy as np
import config

engine = create_engine("mysql+pymysql://{user}:{pw}@{srv}/{db}"
                       .format(user=config.sqluser,
                              pw=config.sqlpwd,
                              srv=config.sqlserver,
                              db=config.sqldb))

blob_service = ContainerClient.from_connection_string(config.blockblob, "model-inputs")

df_roads = pd.read_sql_table(
    "road_information",
    con=engine
)

lst_observasjoner = ['obs00', 'obs06', 'obs12', 'obs18']
lst_dager = ['d0', 'd1', 'd2']
lst_tidsrom = ['00_06', '06_12', '12_18', '18_24']

for index, row in df_roads.iterrows():
    df_model = pd.read_sql(
        "call create_model ('" + row['station_id'] + "');",
        con=engine
    )

    for obs, dag, tid in [(obs, dag, tid) for obs in lst_observasjoner for dag in lst_dager for tid in lst_tidsrom]:
        df_inner_model = df_model.copy()

        for a in lst_observasjoner:
            if a != obs:
                df_inner_model = df_inner_model.drop(df_inner_model.filter(regex=a).columns, axis=1)

        for b in lst_dager:
            if b != dag:
                df_inner_model = df_inner_model.drop(df_inner_model.filter(regex=b).columns, axis=1)

        for c in lst_tidsrom:
            if c != tid:
                df_inner_model = df_inner_model.drop(df_inner_model.filter(regex=c).columns, axis=1)

        for h in range(6,56,6):
            df_inner_model['h' + str(h) + '_wind_bearing_sin'] = np.sin(2 * np.pi * df_inner_model['h' + str(h) + '_wind_bearing']/360.0)
            df_inner_model['h' + str(h) + '_wind_bearing_cos'] = np.cos(2 * np.pi * df_inner_model['h' + str(h) + '_wind_bearing']/360.0)
            df_inner_model.drop(columns=['h' + str(h) + '_wind_bearing'], inplace=True)

        df_inner_model = df_inner_model.interpolate(method ='linear', limit_direction ='both')

        df_inner_model.insert(loc=len(df_inner_model.columns) - 1, column='wind_bearing_sin', value=np.sin(2 * np.pi * df_inner_model[obs+'_wind_bearing']/360.0))
        df_inner_model.insert(loc=len(df_inner_model.columns) - 1, column='wind_bearing_cos', value=np.cos(2 * np.pi * df_inner_model[obs+'_wind_bearing']/360.0))

        def day_this_winter(dt):
            return dt.timetuple().tm_yday - 274 if 0 < dt.timetuple().tm_yday - 274 < 365 else dt.timetuple().tm_yday + 91

        df_inner_model.insert(loc=len(df_inner_model.columns) - 1, column='day_this_winter', 
            value=df_inner_model.apply( lambda row: day_this_winter(datetime.strptime(row['theDate'], '%Y-%m-%d')), axis=1))

        df_inner_model = df_inner_model.drop(['theDate', 'station_id'], axis=1)
        df_inner_model.drop(columns=[obs+'_wind_bearing'], inplace=True)

        output = df_inner_model.to_csv(index=False)
        blob_service.upload_blob(name=row['station_id'] + "_" + obs + "_" + dag + tid + ".csv", data=output, overwrite=True)
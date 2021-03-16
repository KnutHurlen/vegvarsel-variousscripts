import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import config

engine = create_engine("mysql+pymysql://{user}:{pw}@{srv}/{db}"
                       .format(user=config.sqluser,
                              pw=config.sqlpwd,
                              srv=config.sqlserver,
                              db=config.sqldb))

xl_sheets = {
    "SN79791": "E6 Saltfjellet.xlsx", 
    "SN84905": "E10 Bjørnfjell.xlsx", 
    "SN94195": "E6 Sennalandet.xlsx"
    }

for station_id, xl_sheet in xl_sheets.items():

    dt = datetime(2015,1,1)
    dtend = datetime.today()


    data = pd.read_excel(xl_sheet, engine='openpyxl')
    df = pd.DataFrame(data, columns = ['Meldingstype', 'Meldingstekst', 'Gyldig fra', 'Utløpt'])
    df = df[(df.Meldingstype.isin(['Midlertidig stengt', 'Kolonnekjøring']))]
    df = df[(df.Meldingstekst.str.contains('vind|uvær|kjøreforhold|kolonne', case=False))]
    
    dfDaily = pd.DataFrame(columns = \
        ['Date'
        ,'Station_id' \
        , 'Stengt_00_06' \
        , 'Stengt_06_12' \
        , 'Stengt_12_18' \
        , 'Stengt_18_24' \
        , 'Kolonne_00_06' \
        , 'Kolonne_06_12' \
        , 'Kolonne_12_18' \
        , 'Kolonne_18_24' \
        ] \
        )

    while dt < dtend:
        Stengt_00_06 = not df.loc[(df['Meldingstype'] == 'Midlertidig stengt') & (df['Gyldig fra'] <= dt + timedelta(hours=6)) & (df['Utløpt'] > dt + timedelta(hours=0))].empty
        Stengt_06_12 = not df.loc[(df['Meldingstype'] == 'Midlertidig stengt') & (df['Gyldig fra'] <= dt + timedelta(hours=12)) & (df['Utløpt'] > dt + timedelta(hours=6))].empty
        Stengt_12_18 = not df.loc[(df['Meldingstype'] == 'Midlertidig stengt') & (df['Gyldig fra'] <= dt + timedelta(hours=18)) & (df['Utløpt'] > dt + timedelta(hours=12))].empty
        Stengt_18_24 = not df.loc[(df['Meldingstype'] == 'Midlertidig stengt') & (df['Gyldig fra'] <= dt + timedelta(hours=24)) & (df['Utløpt'] > dt + timedelta(hours=18))].empty
        Kolonne_00_06 = not df.loc[(df['Meldingstype'] == 'Kolonnekjøring') & (df['Gyldig fra'] <= dt + timedelta(hours=6)) & (df['Utløpt'] > dt + timedelta(hours=0))].empty
        Kolonne_06_12 = not df.loc[(df['Meldingstype'] == 'Kolonnekjøring') & (df['Gyldig fra'] <= dt + timedelta(hours=12)) & (df['Utløpt'] > dt + timedelta(hours=6))].empty
        Kolonne_12_18 = not df.loc[(df['Meldingstype'] == 'Kolonnekjøring') & (df['Gyldig fra'] <= dt + timedelta(hours=18)) & (df['Utløpt'] > dt + timedelta(hours=12))].empty
        Kolonne_18_24 = not df.loc[(df['Meldingstype'] == 'Kolonnekjøring') & (df['Gyldig fra'] <= dt + timedelta(hours=24)) & (df['Utløpt'] > dt + timedelta(hours=18))].empty
        
        if (any([Stengt_00_06, Stengt_06_12, Stengt_12_18, Stengt_18_24, Kolonne_00_06, Kolonne_06_12, Kolonne_12_18, Kolonne_18_24])):
            dfDaily = dfDaily.append({
                "Date": dt
                ,"Station_id": station_id
                ,"Stengt_00_06": int(Stengt_00_06)
                ,"Stengt_06_12": int(Stengt_06_12)
                ,"Stengt_12_18": int(Stengt_12_18)
                ,"Stengt_18_24": int(Stengt_18_24)
                ,"Kolonne_00_06": int(Kolonne_00_06)
                ,"Kolonne_06_12": int(Kolonne_06_12)
                ,"Kolonne_12_18": int(Kolonne_12_18)
                ,"Kolonne_18_24": int(Kolonne_18_24)
            }, ignore_index=True)
            

        dt += timedelta(days=1)
        
    dfDaily.to_sql('closed_road_history', con=engine, if_exists='append', index=False)


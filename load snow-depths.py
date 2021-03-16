import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
import config

engine = create_engine("mysql+pymysql://{user}:{pw}@{srv}/{db}"
                       .format(user=config.sqluser,
                              pw=config.sqlpwd,
                              srv=config.sqlserver,
                              db=config.sqldb))

dt = date(2015,1,1)
dtend = date.today()

url_list = {
    "SN79791": "https://www.yr.no/nb/historikk/tabell/1-533225/Norge/Nordland/Saltdal/Saltfjellet-Svartisen%20nasjonalpark", 
    "SN84905": "https://www.yr.no/nb/historikk/tabell/5-84900/Norge/Nordland/Narvik/Bj%C3%B8rnfjell", 
    "SN94195": "https://www.yr.no/nb/historikk/tabell/5-94255/Norge/Troms%20og%20Finnmark/Hammerfest/Hammerfest"
    }

while dt < dtend:
    for station_id, baseurl in url_list.items():
        URL = baseurl + "?q=" \
                + str(dt.year) \
                + "-" \
                + str(dt.month).zfill(2)

        df = pd.DataFrame(columns = \
        ['Station_id'
        ,'År' \
        ,'Måned' \
        ,'Dag' \
        ,'Min_temp' \
        ,'Max_temp'
        ,'Gjennomsnitt' \
        ,'Nedbør' \
        ,'Snødybde' \
        ,'Vind' \
        ,'Vindkast' ] \
        )
        
        try:
            page = requests.get(URL).text 
            soup = BeautifulSoup(page, 'lxml')
            body = soup.find('body')
            tbl = body.find('table', class_='fluid-table__table')

            for tr in tbl.tbody.find_all('tr'):
                td = tr.find_all('td')
                df = df.append({
                    "Station_id": station_id
                    ,"År": dt.year
                    ,"Måned": dt.month
                    ,"Dag": td[0].find('span', class_="fluid-table__cell-content").text.replace('.', '').strip()
                    ,"Min_temp": td[1].find('span', class_="fluid-table__cell-content").text.replace('°', '').replace(',','.').replace('–', ' ').strip()
                    ,"Max_temp": td[2].find('span', class_="fluid-table__cell-content").text.replace('°', '').replace(',','.').replace('–', ' ').strip()
                    ,"Gjennomsnitt": td[3].find('span', class_="fluid-table__cell-content").text.replace('°', '').replace(',','.').replace('–', ' ').strip()
                    ,"Nedbør": td[5].find('span', class_="fluid-table__cell-content").text.replace(',','.').replace('–', ' ').strip()
                    ,"Snødybde": td[6].find('span', class_="fluid-table__cell-content").text.replace(',','.').replace('–', ' ').strip()
                    ,"Vind": td[7].find('span', class_="fluid-table__cell-content").text.replace(',','.').replace('–', ' ').replace('-', ' ').strip()
                    ,"Vindkast": td[8].find('span', class_="fluid-table__cell-content").text.replace(',','.').replace('–', ' ').replace('-', ' ').strip()
                }, ignore_index=True)
            df = df.replace(r'^\s*$', np.nan, regex=True)
            print(station_id + ': ' + str(dt.year) + '-' + str(dt.month).zfill(2))
        except:
            print("Error: " + URL)
        finally:
            sleep(np.random.randint(1, 10))
        df.to_sql('snow_depth_observations', con=engine, if_exists='append', index=False)
         
    dt += relativedelta(months=1)


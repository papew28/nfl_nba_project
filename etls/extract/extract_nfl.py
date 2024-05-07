import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def etl_extract_nfl(url):

    data= {
        "team": [],
        "nom": [],
        "position": [],
        "blessure": [],
        "date": [],
        "sport": []
     }

    try:
        response=requests.get(url)
        if response.status_code==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('div', class_='TableBaseWrapper')
            for table in tables:
                   content=table.find('div',{'id':'TableBase'})
                   team=content.find('h4').find('div').find_all('div')[-1].find('span').find('a').text
                   elements=content.find('div',{'class':'TableBase-shadows'}).find('table')
                   rows = elements.find('tbody').find_all('tr')
                   for row in rows:
                          data["team"].append(team)
                          blesser=row.find_all('td')
                          data["nom"].append(blesser[0].find_all('span')[1].find('a').text)
                          data["position"].append(blesser[1].text.strip())
                          data["date"].append(blesser[2].find('span').text.strip())
                          data["blessure"].append(blesser[3].text.strip())
                          data["sport"].append("nfl")           
            pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "data\inputs")+"\data_nba.csv", index=False)
            return data
        else:
            return None
    except Exception as e:
        print(e)
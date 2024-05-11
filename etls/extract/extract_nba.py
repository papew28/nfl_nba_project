from bs4 import BeautifulSoup
#from .outils import get_headers,extract_with_proxies
import requests


from utils.constant import api_key


def etl_extract_nba(url):
   
    data = {
        "team": [],
        "name": [],
        "sport": [],
        "blessure": [],
        "position": [],
        "date": []
    }

    try:
        response =requests.get(url)
        if response.status_code == 200:
              soup = BeautifulSoup(response.content, 'html.parser')
              content=soup.find('div',{'id':"Col1-0-LeagueTeamsInjuries-Proxy"})
              elements=content.find('div').find('ul').find_all('li')
              for element in elements:
                  enregistrements=element.find("div")
                  team=enregistrements.find("div").find("h3").text
                  body=element.find("table")
                  rows=body.find('tbody').find_all('tr')
                  for row in rows:
                     data["team"].append(team)
                     contents=row.find_all('td')
                     data["name"].append(contents[0].find("div").find("a").find("span").text)
                     data["position"].append(contents[1].find("span").text)
                     data["sport"].append("basketball_nba")
                     data["blessure"].append(contents[2].find("span").text)
                     data["date"].append(contents[3].find("span").get("title"))
              return data             
        else:
            return None
        
    except Exception as e:
        print(e)   



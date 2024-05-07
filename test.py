import requests
from bs4 import BeautifulSoup

def etl_extract_nba(url):
   
    data = {
        "team": [],
        "name": [],
        "sport": [],
        "blessure": [],
        "position": [],
        "date": [],
    }

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

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
    except Exception as e:
        print(e)   
a=etl_extract_nba("https://sports.yahoo.com/nba/injuries/")
print(a)


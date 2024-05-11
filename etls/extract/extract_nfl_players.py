import requests
from bs4 import BeautifulSoup
from .outils import get_headers,extract_with_proxies

def get_urls(url):

    response=requests.get(url)
    if response.status_code==200:
       soup=BeautifulSoup(response.content, 'html.parser')
       content=soup.find("div", {"id":"Col1-0-LeaguePlayers-Proxy"})
       content=content.find("div")
       teams_content=content.find("div",{"class":"Mt(20px)"})
       teams=teams_content.find_all("div")
       print(teams)
      


get_urls("https://sports.yahoo.com/nfl/players/")
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests
import pandas as pd
from configparser import ConfigParser
import os

url="https://sports.yahoo.com/"

data={
        "team":[],
        "nom":[],
        "sport":[],
        "position":[],
        "blessure":[],
        "date":[]
    }

options=uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
driver=uc.Chrome(options=options)
driver.get(url)
time.sleep(5)
driver.find_element(By.ID,"root_1").click()
WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID, "root_1_9")))
driver.find_element(By.ID,"root_1_9").click()
WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID, "Col1-0-LeagueTeamsInjuries-Proxy")))
tab=driver.find_element(By.ID,"Col1-0-LeagueTeamsInjuries-Proxy")
elements = tab.find_elements(By.CSS_SELECTOR, 'ul li')
for element in elements:
    rows=element.find_elements(By.CSS_SELECTOR, 'table>tbody>tr')
    for row in rows:
       data["team"].append(element.find_element(By.CSS_SELECTOR, 'div>div>div>span>h3').text)
       data["nom"].append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text)
       data["position"].append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text)
       data["blessure"].append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text)
       data["date"].append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text)
       data["sport"].append("nba")
pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "data")+"\data_nba.csv", index=False)

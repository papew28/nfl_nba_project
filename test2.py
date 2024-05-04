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

url="https://www.cbssports.com/nfl/injuries/"

data={
        "team":[],
        "nom":[],
        "position":[],
        "blessure":[],
        "date":[],
        "sport":[]
    }
try:
       options=uc.ChromeOptions()
       options.add_argument('--headless')
       options.add_argument('--disable-blink-features=AutomationControlled')
       driver=uc.Chrome(options=options)
       driver.get(url)
       time.sleep(5)
       tab=driver.find_element(By.XPATH,"//div[@class='Page-content']/main/div[@class='Page-colMain']")
       elements=tab.find_elements(By.CLASS_NAME,"TableBaseWrapper")
       for element in elements:
              content=element.find_element(By.ID,"TableBase")
              table=content.find_element(By.CLASS_NAME,"TableBase-shadows")
              body=table.find_element(By.CSS_SELECTOR,'div>table>tbody')
              rows=body.find_elements(By.TAG_NAME,"tr")
              for row in rows:
                    data["team"].append(content.find_element(By.CSS_SELECTOR,'h4>div>div:nth-child(2)>div>span>a').text)
                    data["nom"].append(row.find_element(By.CSS_SELECTOR,'td:nth-child(1)>span:nth-child(2)>span>a').text)
                    data["position"].append(row.find_element(By.CSS_SELECTOR,'td:nth-child(2)').text)
                    data["date"].append(row.find_element(By.CSS_SELECTOR,'td:nth-child(3)>span').text)
                    data["blessure"].append(row.find_element(By.CSS_SELECTOR,'td:nth-child(4)').text)
                    data["sport"].append("nfl")
       pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "data")+"\data_nfl.csv", index=False)
       
finally:
       driver.quit()
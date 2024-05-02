import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd
from configparser import ConfigParser
import os


config_parser=ConfigParser()
config_parser.read('./../../config/config.ini')


def extract():

    try:
         options=uc.ChromeOptions()
         options.add_argument('--headless')
         options.add_argument('--disable-blink-features=AutomationControlled')
         driver=uc.Chrome(options=options)
         driver.get(config_parser.get('urls','url'))
         time.sleep(5)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
  

extract()
from configparser import ConfigParser
import undetected_chromedriver as uc
import requests
config_parser=ConfigParser()
config_parser.read('./config/config.ini')

api_key=config_parser.get('api','api_key')

url_nba=config_parser.get('urls','url_nba')
url_nfl=config_parser.get('urls','url_nfl')


print(requests.get(url_nba).text)
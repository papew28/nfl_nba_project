from configparser import ConfigParser

config_parser=ConfigParser()
config_parser.read('./../config/config.ini')

api_key=config_parser.get('api','api_key')

url_nba=config_parser.get('urls','url_nba')
url_nfl=config_parser.get('urls','url_nfl')
from configparser import ConfigParser
config_parser=ConfigParser()
config_parser.read('./config/config.ini')

api_key=config_parser.get('api','api_key')

url_nba=config_parser.get('urls','url_nba')
url_nfl=config_parser.get('urls','url_nfl')

gcp_conn_id=config_parser.get('gcp','gcp_id')
bucket_name=config_parser.get('gcp','gcp_bucket')

print(bucket_name)
print(gcp_conn_id)

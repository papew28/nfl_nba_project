import requests

proxies = []


def get_proxies():
    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': 'bd118ff6-1366-4b17-a221-5df5cc3326e3',
            'url': 'https://sports.yahoo.com/',
        },
    )
    print('Response Body: ', response.json())
   
def send_proxies(proxies):
    good_proxies = []
    with open(proxies, 'r') as f:
         f.readline()  
         for line in f:
             proxy = line.split(',')[0].strip()  
             proxies.append(proxy)
    
    for proxy in proxies:
       try:
             response = requests.get('https://sports.yahoo.com/', proxies={'http': proxy, 'https': proxy}, timeout=5)
             if response.status_code == 200:
                 good_proxies.append(proxy)
            
       except Exception as e:
               print(f"Proxy a échoué avec l'erreur :{e} ")

get_proxies()
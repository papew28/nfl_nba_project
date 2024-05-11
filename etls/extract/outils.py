import requests

proxies = []

def get_headers(api_key):
    response = requests.get(
    url='https://headers.scrapeops.io/v1/browser-headers',
    params={
      'api_key': api_key,
      'num_results': '1'}
    )
    return response.json()["result"][0]["user-agent"]

def extract_with_proxies(url,api_key,headers):
    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': api_key,
            'url': url,
            "headers":headers
        },
    )
    return response
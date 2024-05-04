from etls.extract import extract
from etls.transform import transform
from etls.load import load


def extract_nba(**kwargs):
    url=kwargs['url_nba']
    data=extract(url)

    return data

def extract_nfl(**kwargs):
    url=kwargs['url_nfl']
    data=extract(url)

    return data


def transform(data):
    
    data=transform(data)
    
    return data

def load(data):

    load(data)

    load(data)
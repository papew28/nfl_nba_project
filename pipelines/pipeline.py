from etls.extract.extract_nba import etl_extract_nba
from etls.extract.extract_nfl import etl_extract_nfl
import pandas as pd
import os


def extract_nba(url,**kwargs):
    print(url)
    data=etl_extract_nba(url)
    pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "data\inputs")+"\data_nba.csv", index=False)
    kwargs['ti'].xcom_push(key='nba_data',value=data)
    return "nba_data extracted"

def extract_nfl(url,**kwargs):
    print(url)
    data=etl_extract_nfl(url)
    pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "data\inputs")+"\data_nfl.csv", index=False)
    kwargs['ti'].xcom_push(key='nfl_data',value=data)
    return "nfl_data extracted"




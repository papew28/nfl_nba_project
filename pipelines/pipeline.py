from etls.extract.extract_nba import etl_extract_nba
from etls.extract.extract_nfl import etl_extract_nfl
from etls.transform.transform_nba_data import etl_transform_nba_data
from etls.transform.transfrom_nfl_data import etl_transform_nfl_data
import pandas as pd
import os


def extract_nba(url,**kwargs):
    print(url)
    data_nba=etl_extract_nba(url)
    #pd.DataFrame(data_nba).to_csv(os.path.join(os.getcwd(), "data\inputs")+"\data_nba.csv", index=False)
    print(data_nba)
    kwargs['ti'].xcom_push(key='nba_data',value=data_nba)
    return "nba_data extracted"

def extract_nfl(url,**kwargs):
    data_nfl=etl_extract_nfl(url)
    pd.DataFrame(data_nfl).to_csv(os.path.join(os.getcwd(), "data\inputs")+"\data_nfl.csv", index=False)
    kwargs['ti'].xcom_push(key='nfl_data',value=data_nfl)
    return "nfl_data extracted"

def transform_nba_data(**kwargs):
  
   data=kwargs['ti'].xcom_pull(task_ids='extract_nba',key="nba_data")
   return etl_transform_nba_data(data)

def transform_nfl_data(**kwargs):
  
   data=kwargs['ti'].xcom_pull(task_ids='extract_nfl',key="nfl_data")
   return etl_transform_nfl_data(data)


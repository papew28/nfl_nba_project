from etls.extract.extract_nba import etl_extract_nba
from etls.extract.extract_nfl import etl_extract_nfl
from etls.transform.transform_nba_data import etl_transform_nba_data
from etls.transform.transfrom_nfl_data import etl_transform_nfl_data
import pandas as pd
import json


def extract_nba(url,**kwargs):
    print(url)
    data_nba=etl_extract_nba(url)
    pd.DataFrame(data_nba).to_csv("data/inputs/nba_data.csv", index=False)
    print(data_nba)
    kwargs['ti'].xcom_push(key='nba_data',value=data_nba)
    return "nba_data extracted"

def extract_nfl(url,**kwargs):
    data_nfl=etl_extract_nfl(url)
    with open("data/inputs/nfl_data.json", "w") as json_file:
        json.dump(data_nfl, json_file)
    pd.DataFrame(data_nfl).to_csv("data/inputs/nfl_data.csv", index=False)
    kwargs['ti'].xcom_push(key='nfl_data',value=data_nfl)
    return "nfl_data extracted"

def transform_nba_data(**kwargs):
  
   data=kwargs['ti'].xcom_pull(task_ids='extract_and_transform_nba.extract_nba',key="nba_data")
   transform_data=etl_transform_nba_data(data)
   pd.DataFrame(transform_data).to_csv("data/output/transformed_nba_data.csv", index=False)
   return "nfl_data transformed"

def transform_nfl_data(**kwargs):
  
   data=kwargs['ti'].xcom_pull(task_ids='extract_and_transform_nfl.extract_nfl',key="nfl_data")
   transform_data=etl_transform_nfl_data(data)
   pd.DataFrame(transform_data).to_csv("data/output/transformed_nfl_data.csv", index=False)
   return "nfl_data transformed"


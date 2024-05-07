from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import os
import sys

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.pipeline import extract_nba,extract_nfl
from utils.constant import  url_nba,url_nfl

with DAG("nfl_nba", start_date=datetime(2024,5,7), schedule_interval=None, catchup=False) as dag:

    start=EmptyOperator(task_id="start")

    extract_nfl=PythonOperator(
        task_id="extract_nfl",
        python_callable=extract_nfl,
        provide_context=True,
        op_kwargs={
            "url":url_nfl
        }
    )

    extract_nba=PythonOperator(
       task_id="extract_nba",
       python_callable=extract_nba,
       provide_context=True,
       op_kwargs={
            "url":url_nba
       }
    )

    end=EmptyOperator(task_id="end")

    start>>extract_nba>>extract_nfl>>end
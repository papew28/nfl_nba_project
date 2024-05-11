from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import os
import sys
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.task_group import TaskGroup

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.pipeline import extract_nba,extract_nfl,transform_nba_data,transform_nfl_data
from utils.constant import  url_nba,url_nfl,gcp_conn_id,bucket_name


def upload_fileToGCP(bucket_name, file_path, object_name,gcp_cid):
    hook = GCSHook(gcp_conn_id=gcp_cid)
    hook.upload(bucket_name=bucket_name, object_name=object_name, filename=file_path)


with DAG("nfl_nba", start_date=datetime(2024,5,7), schedule_interval=None, catchup=False) as dag:

    start = EmptyOperator(task_id="start")

    with TaskGroup("extract_and_transform_nba") as extract_and_transform_nba:
        extract_nba_task = PythonOperator(
            task_id="extract_nba",
            python_callable=extract_nba,
            provide_context=True,
            op_kwargs={"url": url_nba}
        )
        

        transform_nba_task = PythonOperator(
            task_id="transform_nba",
            python_callable=transform_nba_data,
            provide_context=True
        )
        extract_nba_task >> transform_nba_task

    with TaskGroup("extract_and_transform_nfl") as extract_and_transform_nfl:
        extract_nfl_task = PythonOperator(
            task_id="extract_nfl",
            python_callable=extract_nfl,
            provide_context=True,
            op_kwargs={"url": url_nfl}
        )

        transform_nfl_task = PythonOperator(
            task_id="transform_nfl",
            python_callable=transform_nfl_data,
            provide_context=True
        )
        extract_nfl_task >> transform_nfl_task

    with TaskGroup("upload_data") as upload_data:
        upload_nfl_file_to_gcs = PythonOperator(
            task_id="upload_nfl_file_to_gcs",
            python_callable=upload_fileToGCP,
            op_kwargs={
                "bucket_name": bucket_name,
                "file_path": "data/output/transformed_nfl_data.csv",
                "object_name": "injuriesdata/nflInjuries_data.csv",
                "gcp_cid": gcp_conn_id
            }
        )

        upload_nba_file_to_gcs = PythonOperator(
            task_id="upload_nba_file_to_gcs",
            python_callable=upload_fileToGCP,
            op_kwargs={
                "bucket_name": bucket_name,
                "file_path": "data/output/transformed_nba_data.csv",
                "object_name": "injuriesdata/nbaInjuries_data.csv",
                "gcp_cid": gcp_conn_id
            }
        )
        upload_nfl_file_to_gcs >> upload_nba_file_to_gcs

    ulpload_to_bigquery = GCSToBigQueryOperator(  
        task_id="ulpload_to_bigquery",
        bucket=bucket_name,
        gcp_conn_id=gcp_conn_id,
        source_objects=["injuriesdata/nflInjuries_data.csv","injuriesdata/nbaInjuries_data.csv"],
        destination_project_dataset_table='infinite-bruin-420816.nfl_nba_data.injuries_data',
        source_format="CSV",
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE"

    )
    

    end = EmptyOperator(task_id="end")

    start >> [extract_and_transform_nba, extract_and_transform_nfl]

    extract_and_transform_nba >> upload_nba_file_to_gcs
    extract_and_transform_nfl >> upload_nfl_file_to_gcs
    
    upload_data >> ulpload_to_bigquery

    ulpload_to_bigquery >> end
    

   
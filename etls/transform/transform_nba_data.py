




def transform_nba_data(**kwargs):

    data=kwargs['ti'].xcom_pull(task_ids='extract_nba')

    
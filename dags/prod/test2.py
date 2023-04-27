import os
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG

default_args = {
                'owner' : 'airflow',
                'depends_on_past' : False,
                'email_on_failure' : False,
                'email_on_retry' : False,
                'retries' : 2,
                'start_date' : datetime(2023, 1, 1),
                # 'retry_delay' : timedelta(seconds = 300),
                'schedule_interval' : '0 0 * * *'
                }
def Hello():
    return 'Hello World!'

with DAG(
    dag_id = 'stock_etl_pipeline2', 
    default_args = default_args,
    catchup=False
    ) as dag:
    extractOperator = PythonOperator(
        task_id = 'extract',
        python_callable = Hello,
        op_args = ["{{ ds_nodash }}"],
        dag = dag
    )
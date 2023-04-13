from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG
import logging

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

def printHello():
    logging.info("hello world!")

with DAG(
    dag_id = 'stock_etl_pipeline', 
    default_args = default_args,
    catchup=False
    ) as dag:

    HelloOperator = PythonOperator(
        task_id = 'printHello',
        python_callable = printHello,
        dag = dag
    )

    HelloOperator

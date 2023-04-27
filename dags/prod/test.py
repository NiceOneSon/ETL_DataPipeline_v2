import datetime
from plugins.Async import GCSAsyncExtractOperator
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
                'catchup' : False,
                'owner' : 'airflow',
                'depends_on_past' : False,
                'email_on_failure' : False,
                'email_on_retry' : False,
                'retries' : 2,
                'start_date' : datetime.datetime(2023, 1, 1),
                'schedule_interval' : '0 0 * * *'
                }


with DAG(dag_id = 'test_thread', default_args=default_args) as dag:
    extract = GCSAsyncExtractOperator(
        execution_date='{{ ds_nodash }}',
        gcp_conn_id = 'gcp_conn_id',
        bucket='kube-airflow-bucket',
        url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?',
        object_path='/test',
        elements=[('serviceKey', 'wKGRs4uOPfXPP1gmBMd619uXkZe0IijRF%2FosAG4iM4BUnCeA7bjNsptqe%2FUS6snti8Ugs9aTBLCImeLuXB4ecQ%3D%3D'),
                ('numOfRows', '2000'),
                ('resultType', 'json')]
    )

    extract
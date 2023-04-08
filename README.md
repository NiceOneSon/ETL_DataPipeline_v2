# ETL_DataPipeline_v2

## Project Goal
기존 ver 1의 문제를 개선함. 기존 문제는 아래와 같음
1) Dataproc
Dataproc
2) Airflow Node Scaling\
두 가지 방안이 존재 CeleryOperator와 KubernetesPodOperator를 사용하는 방법.\
전자의 경우 Refer.2를 보면 알 수있듯 첫째 MQ를 관리해야한다는 점, 둘째 WorkerNode를 모니터링해야한다는 점이 존재.
따라서 Line, 오늘의 집, 쏘카 등은 Kubernetes를 사용한 Scaling을 활용함.



## Refer
### 1. Kubernetes를 이용한 효율적인 데이터 엔지니어링
https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2

### 2. 버킷플레이스 Airflow 도입기
https://www.bucketplace.com/post/2021-04-13-%EB%B2%84%ED%82%B7%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4-airflow-%EB%8F%84%EC%9E%85%EA%B8%B0/

### 3. 쏘카 데이터 그룹 - Airflow와 함께한 데이터 환경 구축기(feat. Airflow on Kubernetes)
https://tech.socarcorp.kr/data/2021/06/01/data-engineering-with-airflow.html

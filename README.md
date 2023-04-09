# ETL_DataPipeline_v2

## Purpose of project
기존 [ver 1](https://github.com/NiceOneSon/ETL_DataPipeline_v1) 데이터 파이프라인의 문제를 개선함.\
기업이 성장하면서 Airflow를 담당하는 Compute Engine의 Scaleup이 아닌 Scaleout을 통해 해결하고자 할 때.

해결하기 위한 두 가지 방안이 존재 CeleryOperator와 KubernetesPodOperator를 사용하는 방법.\
전자의 경우 Refer.2를 보면 알 수있듯 첫째 MQ를 관리해야한다는 점, 둘째 WorkerNode를 모니터링해야한다는 점이 문제로 존재함.\
따라서, 후자인 KubernetesPodOperator를 사용.

## Architecture of Kubernetes



## Refer
### 1. Kubernetes를 이용한 효율적인 데이터 엔지니어링
https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2

### 2. 버킷플레이스 Airflow 도입기
https://www.bucketplace.com/post/2021-04-13-%EB%B2%84%ED%82%B7%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4-airflow-%EB%8F%84%EC%9E%85%EA%B8%B0/

### 3. 쏘카 데이터 그룹 - Airflow와 함께한 데이터 환경 구축기(feat. Airflow on Kubernetes)
https://tech.socarcorp.kr/data/2021/06/01/data-engineering-with-airflow.html

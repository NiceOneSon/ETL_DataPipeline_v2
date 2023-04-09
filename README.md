# ETL_DataPipeline_v2

## Purpose of project
기존 [ver 1](https://github.com/NiceOneSon/ETL_DataPipeline_v1) 데이터 파이프라인의 문제를 개선하기 .\
기업이 성장하면서 Airflow가 담당하는 파이프라인 개수 또는 작업량이 엄청나게 많아진다면? 효율적으로 파이프라인 작업을 어떻게 진행할 수 있을까.\
1. Scale Out\
LocalExecutor 형식으로 처리했던 version 1과 비교할 때 기업의 규모가 커진다면 Scale Up이 아닌 Scale Out 방식으로 활용해야함.\
해결하기 위한 두 가지 방안이 존재 CeleryOperator와 KubernetesPodOperator를 사용하는 방법.\
[Operator 정리](https://www.notion.so/Operators-eb269379975a48be90f6089a03a8f4ec)를 근거로 KubernetesPodOperator를 사용

2. Network Throughput\
Dataproc의 경우 내부 HDFS를 사용하지 않고 Cloud Storage를 사용하는데 이 과정에서 Network의 비용이 많이 들 것이다.\
어떻게 비용을 절감할 수 있을지 고민해볼 것.

## Install Cluster.
### GKE 생성
### 

## Architecture of Kubernetes



## Refer
### 1. Kubernetes를 이용한 효율적인 데이터 엔지니어링
https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2

### 2. 버킷플레이스 Airflow 도입기
https://www.bucketplace.com/post/2021-04-13-%EB%B2%84%ED%82%B7%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4-airflow-%EB%8F%84%EC%9E%85%EA%B8%B0/

### 3. 쏘카 데이터 그룹 - Airflow와 함께한 데이터 환경 구축기(feat. Airflow on Kubernetes)
https://tech.socarcorp.kr/data/2021/06/01/data-engineering-with-airflow.html

### 4. Deploying Airflow on Google Kubernetes Engine with Helm
https://towardsdatascience.com/deploying-airflow-on-google-kubernetes-engine-with-helm-28c3d9f7a26b

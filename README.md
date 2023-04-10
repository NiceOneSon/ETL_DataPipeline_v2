# ETL_DataPipeline_v2

## Purpose of project
이 프로젝트는 Version 1이 가진 효율성 문제를 고민하고 해결하고자 합니다. 고려 사항으로는 크게 아래 두 가지가 존재합니다.\
This project is aimed for The pipeline [ver 1](https://github.com/NiceOneSon/ETL_DataPipeline_v1).\
especially, Version 2 is needed for efficiency of Version 1. There are two types consideration.

1. 병렬 컴퓨팅(Parallel computing)
- Auto Scaling\
스케일 아웃 방식이 필요합니다. 이는 기존 Local VM 위 LocalExecutor를 Execution으로 사용한 지난 Version 1 프로젝트는 데이터 파이프라인이 증가함에 따라 문제가 생길 수 있습니다.\
Using a way having scale-out resources(server) to perform the Operators in parallel, instead of such as LocalExecutor which can perform the pipeline on a single VM and multiprocessing.\
[Operator 정리](https://www.notion.so/Operators-eb269379975a48be90f6089a03a8f4ec)를 근거로 KubernetesPodOperator를 사용\
Based on [operators](https://www.notion.so/Operators-eb269379975a48be90f6089a03a8f4ec), being decided KubernetesPodOperator.

- Multi processing\
만일 데이터가 엄청 많다면 해당 operator 실행 시 너무 많은 시간이 걸릴 수 있다.\
동시성 & 병렬성 제어로 데이터를 가져오는 방법을 고려.

2. Network Throughput
- Shuffling\
Dataproc의 경우 클러스터 내부 HDFS를 사용하지 않고 외부의 Cloud Storage를 사용하는데 이 과정에서 처리해야할 데이터가 많을 수록 Network의 비용이 많이 들 것이다.\
어떻게 비용을 절감할 수 있을지 고민해볼 것.


## Installation for Airflow cluster.
두 가지를 참고.
1. Airflow Cluster 설치\
[Deploying Airflow on Google Kubernetes Engine with Helm](https://towardsdatascience.com/deploying-airflow-on-google-kubernetes-engine-with-helm-28c3d9f7a26b)

2. 
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

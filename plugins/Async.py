###
# User Defined Funtions
# 1. Class
#    a. Extract : 비동기 방식으로 서버의 데이터를 크롤링해오는 객체 생성 및 작업 수행.(2022-04-18)
### 

import os
import logging
import tempfile
import requests
import pandas as pd
import threading

from typing import List, Tuple, Mapping, Any
from pandas.core.api import DataFrame
from airflow.models import BaseOperator
from airflow.utils.context import Context, context_merge
from concurrent.futures import ThreadPoolExecutor, as_completed
from airflow.providers.google.cloud.operators.gcs import GCSHook

class GCSAsyncExtractOperator(BaseOperator, GCSHook):
    def __init__(self,
                execution_date: str,
                url: str, 
                gcp_conn_id: str,
                bucket: str,
                object_path: str,
                op_kwargs: Mapping[str, Any],
                elements: List[Tuple[str, str]],
                **kwargs
                ):
        """
        execution_date : When is the time to extract.
        url : Server url is needed.
        gcp_conn_id : The connection id to connect google cloud platform 
        bucket : where is the bucket to store.
        object_path : what object name to store.
        elements : elements to add on the url.
        """
        BaseOperator.__init__(**kwargs)
        GCSHook(gcp_conn_id=gcp_conn_id)
        self.op_kwargs = op_kwargs
        self.executionDate = execution_date
        self.url = url
        self.bucket = bucket
        self.object = object_path
        self.elements = elements
        self.lock = threading.Lock()
        self.num_of_thread = 3
        self.page = 0

        if self.elements == None:
            logging.info('No elements inserted.')
        
        

    def get_json(self, page: int) -> dict:
        url = self.url
        executionDate = self.executionDate
        
        if page == None:
            raise ValueError('Page is required.')

        for element, val in self.elements:
            url += f'&{element}={val}'
        url += f'&pageNo={page}'
        url += f'&basDt={self.executionDate}'
        result = requests.get(url)

        if result.status_code != 200:
            return False
        if not result.content:
            return False
        
        jsonResult = result.json()['response']['body']['items']['item']

        if not jsonResult:
            return False
        
        logging.info(f'Successfully received the message on the Execution Date :\
                      {executionDate} and url : {url} received\n')
        
        return jsonResult
    
    
    def makeDF(self,
               results: List[dict])-> DataFrame: 
        dataframe = pd.DataFrame()
        return dataframe

    def StoreJson(self, 
                  result: dict
                  )-> None:
        bucket = self.bucket
        objectName = self.object

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, f'tempDF_{objectName}.json')
            with open(tmp_path, 'w') as f:
                import json
                json.dump(result, f)
            self.upload(
                bucket_name = bucket,
                object_name = objectName,
                filename = tmp_path,
            )
            logging.info(f'The file is completely inserted.')

    def thread_crawling(self):
        return_value = {}
        submitteds = set()
        control = True
        num_of_thread = self.num_of_thread
        lock, page = self.lock, self.page
        logging.info('Crawling start!')
        
        with ThreadPoolExecutor(max_workers=num_of_thread) as executor:
            for _ in range(num_of_thread):
                with lock:
                    page += 1
                submitteds.add(executor.submit(self.get_json, page))
            while control:
                with lock:
                    page += 1
                for submitted in as_completed(submitteds):
                    result = submitted.result()
                    if result == False:
                        control = False
                        break
                    with lock:
                        page += 1
                    return_value.update(result)
                    submitteds.remove(submitted)
                    submitteds.add(executor.submit(self.get_json, page))
        logging.info('Crawling Finished!')
        return return_value
    

    def execute(self, **context: Context)-> None: # return type : list[dict]
        context_merge(context, self.op_kwargs)
        result = self.thread_crawling()
        self.StoreJson(result)
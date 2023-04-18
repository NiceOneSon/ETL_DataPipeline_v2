###
# UDF : User Defined Funtions
# Class
# 1. Extract : 비동기 방식으로 서버의 데이터를 크롤링해오는 객체 생성 및 작업 수행.(2022-04-18)
### 

import os
import logging
import tempfile
import requests
import pandas as pd
import threading
import asyncio
import aiohttp

from typing import List, Tuple
from pandas.core.api import DataFrame
from concurrent.futures import ThreadPoolExecutor, as_completed
# from airflow.providers.google.cloud.operators.gcs import GCSHook

class Extract():
    def __init__(self,
                execution_date: str,
                url: str, 
                bucket: str,
                object_path: str,
                params: List[Tuple[str, str]]
                ):
        """
        execution_date : When is the time to extract.
        url : Server url is needed.
        bucket : where is the bucket to store.
        object_path : what object name to store.
        params : parameters to add on the url.
        """
        self.executionDate = execution_date
        self.url = url
        self.bucket = bucket
        self.object = object_path
        self.params = params
        self.lock = threading.Lock()
        self.num_of_thread = 3
        self.page = 0

        if self.params == None:
            logging.info('No params inserted.')
        
        

    def extract(self, page):
        url = self.url
        executionDate = self.executionDate

        for param, val in self.params:
            url += f'&{param}={val}'
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

    def StoreJson(self, 
                  dataframe: DataFrame,
                  bucket: str, 
                  objectName: str):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, f'tempDF_{self.page}.csv')
            dataframe.to_csv(tmp_path, index = False)
            gcs_hook = GCSHook(gcp_conn_id='gcp')
            gcs_hook.upload(
                bucket_name = bucket,
                object_name = objectName,
                filename = tmp_path,
            )
            logging.info(f'The file is completely inserted.')

    def execute(self): # return type : DataFrame
        results = []
        num_of_thread = self.num_of_thread
        control = True
        lock, page = self.lock, self.page
        print('before start!')
        submitteds = set()
        with ThreadPoolExecutor(max_workers=num_of_thread) as executor:
            
            for _ in range(num_of_thread):
                with lock:
                    page += 1

                submitteds.add(executor.submit(self.extract, page))
            
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
                    results.append(result)
                    submitteds.remove(submitted)
                    submitteds.add(executor.submit(self.extract, page))

        print('execute finishied!')
        print(result)
        # dataframe = pd.DataFrame(result)

        # self.StoreJson(dataframe=dataframe,
        #                bucket=self.bucket,
        #                objectName= self.object)
        return results
    
        
        

if __name__ == '__main__':
    import time
    s = time.time()
    ext = Extract(
        execution_date='20230417',
        url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?',
        bucket = None,
        object_path=None,
        params=[('serviceKey', 'wKGRs4uOPfXPP1gmBMd619uXkZe0IijRF%2FosAG4iM4BUnCeA7bjNsptqe%2FUS6snti8Ugs9aTBLCImeLuXB4ecQ%3D%3D'),
                ('numOfRows', '2000'),
                ('resultType', 'json')]
    )
    result = ext.execute()
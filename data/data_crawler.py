import requests
import logging
import time

from bs4 import BeautifulSoup

from data.load_static import *
from data.sql_db import *
from utils.utils import *


def setup_query_list(startYear, endYear):
    regionCode = load_region_code(regionCodeDir)
    dateList = date_generator(startYear, endYear)
    
    queryCnt = 0
    
    queryList = []
    
    for region in range(len(regionCode)):
        for date in range(len(dateList)):
            if dateList[date][0:4] in ('2018', '2019', '2020'):
                serviceKey = serviceKeyList[0]
            elif dateList[date][0:4] in ('2021', '2022', '2023'):
                serviceKey = serviceKeyList[1]
            elif dateList[date][0:4] in ('2015', '2016', '2017'):
                serviceKey = serviceKeyList[2]
                
            queryParams = (serviceUrl + 
                        'LAWD_CD=' + str(regionCode[region][0]) + 
                        '&DEAL_YMD=' + str(dateList[date]) + 
                        '&numOfRows=' + str(100) + 
                        '&serviceKey=' + serviceKey)
        
            queryCnt += 1
            queryList.append(queryParams)

        regionLength = len(regionCode)
        regionIndex = region + 1
        queryLength = len(regionCode) * len(dateList)
        msg = f'[{regionIndex} / {regionLength}] {regionCode[region][2]} Crawling Lists are Created => Total [{queryCnt} / {queryLength} Objects]'
        print(msg, "\n")
        
    return queryList
    
def crawler(startYear, endYear):
    conn, cursor = connect_db('AptTradeDB')
    create_table_query('AptTradeDB', 'tbl_trade')
    
    queryList = setup_query_list(startYear, endYear)
    
    observeCnt = 0
        
    for query in range(len(queryList)):
        response = requests.get(queryList[query])
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        itemList = soup.find_all('item')
        resultList = soup.find_all('header')
        
        time.sleep(0.1)
        
        queryLength = len(queryList)
        queryIndex = query + 1
        insertCnt = 0
        
        insertList = []
        
        for result in resultList:
            resultCode = result.find('resultCode').string.strip()
            resultMsg = result.find('resultMsg').string.strip()
            
        try:
            for item in range(len(itemList)):
                year = itemList[item].find('년').string.strip()
                month = itemList[item].find('월').string.strip()
                day = itemList[item].find('일').string.strip()
                price = itemList[item].find('거래금액').string.strip()
                code = itemList[item].find('지역코드').string.strip()
                dong_name = itemList[item].find('법정동').string.strip()
                jibun = itemList[item].find('지번').string.strip()
                con_year = itemList[item].find('건축년도').string.strip()
                apt_name = itemList[item].find('아파트').string.strip()
                area = itemList[item].find('전용면적').string.strip()
                floor = itemList[item].find('층').string.strip()
                
                insert = [year, month, day, price, code, dong_name, jibun, con_year, apt_name, area, floor]
                insertList.append(insert)
                insertCnt += 1
                
        except Exception as e:
            getResultMsg = f'[API GET RESULT] => [{resultCode} / {resultMsg}]'
            print(getResultMsg, "\n")
            if isinstance(e, AttributeError):
                print(f'[ATTRIBUTE ERROR] => {e}', "\n")
            elif isinstance(e, ValueError):
                print(f'[VALUE ERROR] => {e}', "\n")
            else:
                print(f'[ERROR] => {e}', "\n")
        
        insert_query(conn, cursor, 'tbl_trade', insertList)
        observeCnt += insertCnt
        
        print(f'[PROCESSING] => Index : [{queryIndex} / {queryLength}] \t Inserted : [{insertCnt}] \t Observed : [{observeCnt}]', "\n")
                
    cursor.close()
    conn.close()
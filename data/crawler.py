import requests
import time

from bs4 import BeautifulSoup

from data.static import *
from data.query import *
from utils.utils import *


def setup_query_list(startYear, endYear):
    create_folder('./log')
    setQueryLogger = logger('setup_query_list', './log/setup_query_list.log')
    
    dateList = date_generator(startYear, endYear)
    regionCode = import_data('AptTradeDB', 'tbl_region_code', '50')
    
    queryCnt = 0
    
    queryList = []
    try:
        for region in range(len(regionCode)):
            for date in range(len(dateList)):
                if dateList[date][0:4] in ('2015', '2016', '2017'):
                    serviceKey = serviceKeyList[0]
                elif dateList[date][0:4] in ('2018', '2019', '2020'):
                    serviceKey = serviceKeyList[1]
                elif dateList[date][0:4] in ('2021', '2022', '2023', '2024'):
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
            msg = f'[{regionIndex} / {regionLength}] {regionCode[region][2]} Crawling Lists are Created => [{queryCnt} / {queryLength} Objects]'
            setQueryLogger.info(msg)
        
        return queryList
        
    except Exception as e:
        setQueryLogger.error(f'[QUERY SETUP ERROR] => [{e}]')
        
def crawler(startYear, endYear):
    create_folder('./log')
    crawlerLogger = logger('crawler', './log/crawler.log')
    
    conn, cursor = connect_db('AptTradeDB')
    
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
            crawlerLogger.error(getResultMsg)
            if isinstance(e, AttributeError):
                crawlerLogger.error(f'[ATTRIBUTE ERROR] => [{e}]')
            elif isinstance(e, ValueError):
                crawlerLogger.error(f'[VALUE ERROR] => [{e}]')
            else:
                crawlerLogger.error(f'[ERROR] => [{e}]')
        
        insert_data(conn, cursor, 'tbl_trade_test', insertList, tblTradeTestTotalCols)
        observeCnt += insertCnt
        
        crawlerLogger.info(f"[PROCESSING] => Index : [{queryIndex} / {queryLength}] \t Inserted : [{insertCnt}] \t Observed : [{observeCnt}]")
                
    cursor.close()
    conn.close()
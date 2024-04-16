import re
import pandas as pd

from data.query import *
from data.static import *


def preprocessing(limit):
    rawData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade', limit), columns = tblTradeTotalCols)
    # rawData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade_test', limit), columns = tblTradeTestTotalCols)
    regionCode = pd.DataFrame(import_data('AptTradeDB', 'tbl_region_code', limit), columns = tblRegionCodeTotalCols)
    
    data = rawData.dropna()
    
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    data['ymd'] = pd.to_datetime(data['year'].astype(str) + data['month'].astype(str).str.zfill(2) + data['day'].astype(str).str.zfill(2))
    data['ym'] = data['ymd'].dt.to_period('M').dt.to_timestamp()
    
    data['year'] = data['year'].astype(int)
    data['code'] = data['code'].astype(str)
    data['price'] = data['price'].astype(str).str.replace(',', '').astype(int)
    data['price_unit'] = data['price'].astype(float) / 10000
    data['apt_name'] = (data['apt_name'].astype(str).apply(lambda x: re.sub(r'\(.*?\)', '', x))).astype(str)
    data['con_year'] = data['con_year'].astype(int)
    data['area'] = data['area'].astype(float).round(0)
    data['floor'] = data['floor'].astype(int).abs()
    
    data = pd.merge(data, regionCode, on='code', how='left')
    
    data['addr_1'] = data['addr_1'].astype(str)
    data['district_kr'] = data['sigungu'].astype(str)
    data['district_en'] = data['district_en'].astype(str)
    data['address'] = (data['addr_2'] + ' ' + data['dong_name'] + ' ' + data['jibun'] + ' ' + data['apt_name']).astype(str)
    data['py'] = round(((data['price'] / data['area']) * 3.3), 0)
    data['py_unit'] = data['py'] / 10000
    data['cnt'] = 1
    
    data = data[['ymd', 'ym', 'year', 'code', 'district_kr', 'district_en', 'addr_1', 'apt_name', 'address', 'price', 'price_unit', 'con_year', 'area', 'floor', 'py', 'py_unit', 'cnt']]
    data = data.sort_values('ymd')
    
    print('[BEFORE COUNTS] => [', len(data), ']', '\n')
    
    data = data.drop_duplicates()
    
    print('[AFTER COUNTS] => [', len(data), ']', '\n')
        
    return data
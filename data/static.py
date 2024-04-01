import numpy as np
import pandas as pd


regionCodeDir = './static/base/sigun_code/sigun_code.csv'
def load_region_code(dir):
    data = pd.read_csv(dir)
    data['code'] = data['code'].astype('str')
    data = list(data.itertuples(index=False))
    
    return data

serviceUrl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'
serviceKeyList = [
    'zQmrgI9nisUYc02XtcrSBozXS0f62E3570La3uNCtsoEGKWyHkcJ%2F2lsjpFpQQ5OfdJcsmjpjGQWtt215ZWI%2FQ%3D%3D',
    'yzRqa2hgVHQ85Zhay2GZvoXjTVyVZmYOB%2FnqiH03lQqL%2FEMFgiI69tj%2FQ8xvbe2b9B%2Fe5zgqACDzyy9xZ5AJEw%3D%3D',
    'QNUU8DYwLc3MwlKwjxh4x%2FSBFeIJuBygoLpssxBVKH%2BucHKt0HfnaQ9ozSYlHc%2FuS9odQYgxK5Xysmgs8kjkXQ%3D%3D'
]

tblTradeSchemasDict = {
    'year': 'CHAR(4)',
    'month': 'VARCHAR(2)',
    'day': 'VARCHAR(2)',
    'price': 'VARCHAR(40)',
    'code': 'CHAR(5) NOT NULL',
    'dong_name': 'VARCHAR(40)',
    'jibun': 'VARCHAR(10)',
    'con_year': 'CHAR(4)',
    'apt_name': 'VARCHAR(40)',
    'area': 'VARCHAR(20)',
    'floor': 'VARCHAR(4)'
}

tblTradeOrderDict = {
    'year': 'DESC',
    'month': 'DESC',
    'day': 'DESC',
    'code': 'DESC',
    'apt_name': 'DESC',
    'floor': 'DESC'
}

tblTradeTotalCols = [
    'year', 'month', 'day', 'price', 'code', 'dong_name', 'jibun', 'con_year', 'apt_name', 'area', 'floor'
]

tblRegionCodeSchemasDict = {
    'code': 'CHAR(5) NOT NULL',
    'sido': 'VARCHAR(50)',
    'sigungu': 'VARCHAR(50)',
    'addr_1': 'VARCHAR(50)',
    'addr_2': 'VARCHAR(50)'
}

tblRegionCodeOrderDict = {
    'code': 'DESC',
    'sido': 'DESC',
    'sigungu': 'DESC',
    'addr_1': 'DESC',
    'addr_2': 'DESC'
}

tblRegionCodeTotalCols = [
    'code', 'sido', 'sigungu', 'addr_1', 'addr_2'
]
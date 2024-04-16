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

tblRegionCodeTotalCols = [
    'code', 'sido', 'sigungu', 'district_en', 'addr_1', 'addr_2'
]

tblTradeProcessSchemasDict = {
    'ymd': 'DATE', 
    'ym': 'DATE', 
    'year': 'INT', 
    'code': 'CHAR(5) NOT NULL', 
    'district_kr': 'VARCHAR(5)', 
    'district_en': 'VARCHAR(15)',
    'addr_1': 'VARCHAR(10)', 
    'apt_name': 'VARCHAR(50)', 
    'address': 'VARCHAR(50)', 
    'price': 'INT',
    'price_unit': 'FLOAT',
    'con_year': 'INT', 
    'area': 'FLOAT', 
    'floor': 'INT', 
    'py': 'FLOAT', 
    'py_unit': 'FLOAT', 
    'cnt': 'INT'
}

# tblTradeProcessTotalCols = [
#     'ymd', 
#     'ym', 
#     'year', 
#     'code', 
#     'district_kr', 
#     'district_en', 
#     'addr_1', 
#     'apt_name',
#     'address', 
#     'price', 
#     'price_unit',
#     'con_year',
#     'area', 
#     'floor',
#     'py',
#     'py_unit',
#     'cnt'
# ]

tblTradeProcessTotalCols = [
    'year', 
    'district_en', 
    'price_unit',
    'con_year',
    'area', 
    'floor',
    'py_unit',
]

tblTradeTestSchemasDict = {
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

tblTradeTestTotalCols = [
    'year', 'month', 'day', 'price', 'code', 'dong_name', 'jibun', 'con_year', 'apt_name', 'area', 'floor'
]

tblTradeTestProcessSchemasDict = {
    'ymd': 'DATE', 
    'ym': 'DATE', 
    'year': 'INT', 
    'code': 'CHAR(5) NOT NULL', 
    'district_kr': 'VARCHAR(5)', 
    'district_en': 'VARCHAR(15)',
    'addr_1': 'VARCHAR(10)', 
    'apt_name': 'VARCHAR(50)', 
    'address': 'VARCHAR(50)', 
    'price': 'INT',
    'price_unit': 'FLOAT',
    'con_year': 'INT', 
    'area': 'FLOAT', 
    'floor': 'INT', 
    'py': 'FLOAT', 
    'py_unit': 'FLOAT', 
    'cnt': 'INT'
}

# tblTradeTestProcessTotalCols = [
#     'ymd', 
#     'ym', 
#     'year', 
#     'code', 
#     'district_kr', 
#     'district_en', 
#     'addr_1', 
#     'apt_name',
#     'address', 
#     'price', 
#     'price_unit',
#     'con_year',
#     'area', 
#     'floor',
#     'py',
#     'py_unit',
#     'cnt'
# ]

tblTradeTestProcessTotalCols = [
    'year', 
    'district_en', 
    'price_unit',
    'con_year',
    'area', 
    'floor',
    'py_unit',
]
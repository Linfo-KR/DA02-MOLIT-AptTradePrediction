import pandas as pd
import numpy as np


regionCodeDir = './static/base/sigun_code/sigun_code.csv'

serviceUrl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'
serviceKeyList = [
    'zQmrgI9nisUYc02XtcrSBozXS0f62E3570La3uNCtsoEGKWyHkcJ%2F2lsjpFpQQ5OfdJcsmjpjGQWtt215ZWI%2FQ%3D%3D',
    'yzRqa2hgVHQ85Zhay2GZvoXjTVyVZmYOB%2FnqiH03lQqL%2FEMFgiI69tj%2FQ8xvbe2b9B%2Fe5zgqACDzyy9xZ5AJEw%3D%3D',
    'QNUU8DYwLc3MwlKwjxh4x%2FSBFeIJuBygoLpssxBVKH%2BucHKt0HfnaQ9ozSYlHc%2FuS9odQYgxK5Xysmgs8kjkXQ%3D%3D'
]

def load_region_code(dir):
    regionCode = pd.read_csv(dir, encoding='utf8')
    regionCode['code'] = regionCode['code'].astype('str')
    regionCode = np.array(regionCode)
    
    return regionCode
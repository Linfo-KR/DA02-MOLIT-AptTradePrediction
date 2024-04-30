import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from data.query import *


def load_data(data, pretrainData):
    regionList = pd.DataFrame(import_data('AptTradeDB', 'tbl_region_code', 'district_en', '30'), columns=['region']).values.tolist()
    regionList = [element for sublist in regionList for element in sublist]
    
    selectCols = ['year', 'district_en', 'price_unit', 'con_year', 'area', 'floor', 'py_unit']
    
    originData = data[selectCols]
    pretrainData = pretrainData[selectCols]
    
    district = originData.pop('district_en')
    districtPretrain = pretrainData.pop('district_en')

    for d in regionList:
        originData[f'{d}'] = (district == d) * 1.0
        pretrainData[f'{d}'] = (districtPretrain == d) * 1.0
            
    cols = list(originData.columns)
    
    dependentVar = ['price_unit']
    independentVars = [col for col in cols if col != dependentVar[0]]
    
    trainData, testData = train_test_split(originData, test_size=0.2, shuffle=True, random_state=500)
    trainX = trainData[independentVars]
    trainY = trainData[dependentVar]
    testX = testData[independentVars]
    testY = testData[dependentVar]
    pretrainX = pretrainData[independentVars]
    pretrainY = pretrainData[dependentVar]
    
    trainNormX = trainX.copy()
    testNormX = testX.copy()
    pretrainNormX = pretrainX.copy()
    
    scalerDict = {}
    
    for cols in ['year', 'con_year', 'area', 'floor', 'py_unit']:
        scalerX = MinMaxScaler()
        trainNormX[cols] = scalerX.fit_transform(trainNormX[[cols]])
        testNormX[cols] = scalerX.transform(testNormX[[cols]])
        pretrainNormX[cols] = scalerX.transform(pretrainNormX[[cols]])
        scalerDict[cols] = scalerX
            
    return trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY
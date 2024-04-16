import time
import warnings
import multiprocessing
import re

import pandas as pd
import statsmodels.api as sm

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from data.query import *
from utils.utils import *

warnings.filterwarnings('ignore')


class RegressionModel:
    def __init__(self, data, pretrainData):
        self.data = data
        self.pretrainData = pretrainData
    
    
    def _load_data(self):
        regionList = pd.DataFrame(import_data('AptTradeDB', 'tbl_region_code', 'district_en', '30'), columns=['region']).values.tolist()
        regionList = [element for sublist in regionList for element in sublist]
        
        selectCols = ['year', 'district_en', 'price_unit', 'con_year', 'area', 'floor', 'py_unit']
        
        originData = self.data[selectCols]
        pretrainData = self.pretrainData[selectCols]
         
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
    
    
    def _reg_summary(self, trainNormX, trainY):
        model = sm.OLS(trainY, trainNormX)
        history = model.fit()
        print(history.summary())
        
        with open('./results/reg/summary.txt', 'w') as f:
            f.write(history.summary().as_text())
    
    
    def _run_process(self, model, trainNormX, testNormX, trainY, testY):
        lenTrain = len(trainNormX) + 1
        batch = 10173
        trainLossList, testLossList = [], []
        modelFinal = None
        evalTrain = None
        predY = None
        
        for epoch in range(1, (lenTrain + 1), batch):
            model.fit(trainNormX[:epoch], trainY[:epoch])
            
            trainPredY = model.predict(trainNormX[:epoch])
            testPredY = model.predict(testNormX)
            trainLoss = Metrics(trainY[:epoch], trainPredY).MSE()
            testLoss = Metrics(testY, testPredY).MSE()
            trainLossList.append(trainLoss)
            testLossList.append(testLoss)

            if epoch == 1 or (epoch - 1) % batch == 0 or epoch == lenTrain:
                print(f'Epoch {epoch}/{lenTrain}\nloss: {trainLoss} - val_loss: {testLoss} \n')
                
            if epoch == lenTrain:
                modelFinal = model
                # coef = np.round(modelFinal.coef_, 4)
                # intercept = np.round(modelFinal.intercept_, 4)
                # formula = f'({coef})x + {intercept}'
                evalTrain = np.round(modelFinal.score(testNormX, testY), 2)
                predY = modelFinal.predict(testNormX)
                
        return modelFinal, evalTrain, predY, trainLossList, testLossList
    
    
    def run_regression(self):
        trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY = self._load_data()
        sTime = time.time()
        
        model = LinearRegression()
        modelFinal, evalTrain, predY, trainLossList, testLossList = self._run_process(model, trainNormX, testNormX, trainY, testY)
        
        eTime = time.time()
        
        self._reg_summary(trainNormX, trainY)
        observe_reg_training(testY, predY, trainLossList, testLossList, sTime)
        save_reg_result(modelFinal, testY, predY, evalTrain, sTime, eTime)
        
        pretrainModel = modelFinal
        pretrainPredY = pretrainModel.predict(pretrainNormX)
        save_reg_pretrain_result(pretrainY, pretrainPredY, sTime)
    
    
    # Parallel Computing Test(Memory Error)     
    # def _run_process(self, model, trainNormX, testNormX, trainY, testY, epoch):
    #     model.fit(trainNormX[:epoch], trainY[:epoch])
            
    #     trainPredY = model.predict(trainNormX[:epoch])
    #     testPredY = model.predict(testNormX[:epoch])
    #     trainLoss = Metrics(trainY[:epoch], trainPredY).MSE()
    #     testLoss = Metrics(testY[:epoch], testPredY).MSE()
        
    #     return trainLoss, testLoss, epoch, model
    
    
    # def run_regression(self):
    #     trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY = self._load_data()
    #     lenTrain = len(trainNormX)
    #     batch = 1000
    #     trainLossList, testLossList = [], []
        
    #     sTime = time.time()
        
    #     pool = multiprocessing.Pool()
    #     parallelResults = []
        
    #     model = LinearRegression()
        
    #     for epoch in range(1, lenTrain, batch):
    #         result = pool.apply_async(self._run_process(model, trainNormX, testNormX, trainY, testY, epoch))
    #         parallelResults.append(result)
        
    #     pool.close()
    #     pool.join()
        
    #     for result in parallelResults:
    #         trainLoss, testLoss = result.get()
    #         trainLossList.append(trainLoss)
    #         testLossList.append(testLoss)
            
    #         if epoch == 1 or epoch % 5000 == 0 or epoch == lenTrain:
    #             print(f'Epoch {epoch}/{lenTrain}\nloss: {trainLoss} - val_loss: {testLoss} \n')
                
    #         if epoch == lenTrain:
    #             modelFinal = model
    #             coef = round(modelFinal.coef_, 4)
    #             intercept = round(modelFinal.intercept_, 4)
    #             formula = f'({coef})x + {intercept}'
    #             evalTrain = round(modelFinal.score(testNormX, testY), 2)
    #             predY = modelFinal.predict(testNormX)
                
    #     eTime = time.time()
        
    #     observe_reg_training(testY, predY, trainLossList, testLossList, sTime)
    #     save_reg_result(modelFinal, testY, predY, coef, intercept, formula, evalTrain, sTime, eTime)
        
    #     pretrainModel = modelFinal
    #     pretrainPredY = pretrainModel.predict(pretrainNormX)
    #     save_reg_pretrain_result(pretrainY, pretrainPredY, sTime)
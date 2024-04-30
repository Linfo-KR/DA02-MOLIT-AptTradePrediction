import time
import warnings

import pandas as pd
import statsmodels.api as sm

from sklearn.linear_model import LinearRegression

from data.query import *
from data.load_data import *
from utils.utils import *

warnings.filterwarnings('ignore')


class RegressionModel:
    def __init__(self, data, pretrainData):
        self.data = data
        self.pretrainData = pretrainData

    
    
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
                evalTrain = np.round(modelFinal.score(testNormX, testY), 2)
                predY = modelFinal.predict(testNormX)
                
        return modelFinal, evalTrain, predY, trainLossList, testLossList
    
    
    def run_regression(self):
        trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY = load_data(self.data, self.pretrainData)
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
import multiprocessing
import time
import json

import pandas as pd
import tensorflow as tf

from tensorflow.keras.callbacks import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.regularizers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from data.preprocessing import *
from models.cuda import *
from utils.utils import *


# 회귀모형
# DNN
# Factors = [district, year, con_year, area, floor, py] => Grid Search
# OnehotEncoding => [district]
# Label = [price]

class RegressionModel:
    def __init__(self, data):
        self.data = data
    
    def load_data(self):
        pass
    
    def build_regression():
        pass
    
    def run_regression():
        pass
    
    
class DNN:
    def __init__(self, configs, data):
        self.configs = configs
        self._load_config()
        self.data = data
        self.cores = multiprocessing.cpu_count()
        
        print('\n\n', f'[MAX CPU CORES] => [{self.cores} Objects]', '\n\n')
        
    def _load_config(self):
        with open(self.configs, 'r') as f:
            self.config = json.load(f)
            
        self.layers = self.config.get('layers')
        self.neurons = self.config.get('neurons')
        self.activations = self.config.get('activations')
        self.drs = self.config.get('drs')
        self.lrs = self.config.get('lrs')
        self.lds = self.config.get('lds')
        self.epochs = self.config.get('epochs')
        self.batchs = self.config.get('batchs')
    
    def _load_data(self):
        selectCols = ['year', 'district_en', 'con_year', 'area', 'floor', 'py_unit', 'price_unit']
        originData = self.data[selectCols]
        district = originData.pop('district_en')

        for d in district.unique():
            originData[f'{d}'] = (district == d) * 1.0
        
        cols = list(originData.columns)
        
        dependentVar = ['price_unit']
        independentVars = [col for col in cols if col != dependentVar[0]]
        
        trainData, testData = train_test_split(originData, test_size=0.2, shuffle=False)
        trainX = trainData[independentVars]
        trainY = trainData[dependentVar]
        testX = testData[independentVars]
        testY = testData[dependentVar]
        
        trainNormX = trainX.copy()
        testNormX = testX.copy()
        
        scalerDict = {}
        
        for cols in independentVars:
            scalerX = MinMaxScaler()
            trainNormX[cols] = scalerX.fit_transform(trainNormX[[cols]])
            testNormX[cols] = scalerX.transform(testNormX[[cols]])
            scalerDict[cols] = scalerX
        
        return trainNormX, testNormX, trainY, testY
    
    def _build_dnn(self, layers, neurons, activations, drs, lrs, lds, trainDataX):
        strategy = gpu_using()
        
        with strategy.scope():
            unit = 2
            
            model = Sequential()
            model.add(Dense(unit ** neurons, input_shape=[len(trainDataX.keys())]))
            
            for layer in range(1, layers + 1):
                model.add(Dense(unit ** neurons, activation=activations, kernel_regularizer=l2(lds)))
                model.add(BatchNormalization())
                model.add(Dropout(rate=drs))
                
            model.add(Dense(unit ** 0))
            
            optimizer = tf.keras.optimizers.Adam(lr=lrs)
            model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['mae'])
            model.summary()
            
            numLayers = 0
            for layer in model.layers:
                if isinstance(layer, Dense):
                    numLayers += 1
                    
                for weight in layer.weights:
                    print(f'Layer : {layer.name}, Parameter : {weight.name}, Data Type : {weight.dtype}')
                    
            numLayers = numLayers - 2
            numNeurons = [layer.units for layer in model.layers if isinstance(layer, Dense)]
            
        return model, numLayers, numNeurons
    
    def run_dnn(self):
        trainNormX, testNormX, trainY, testY = self._load_data()
        for layer in self.layers:
            for neuron in self.neurons:
                for activation in self.activations:
                    for dr in self.drs:
                        for lr in self.lrs:
                            for ld in self.lds:
                                for epoch in self.epochs:
                                    for batch in self.batchs:
                                        sTime = time.time()
                                        
                                        initLd = 0.1
                                        weightLd = 1.1
                                        lambdaL2 = initLd * (weightLd ** ld)
                                        
                                        model, numLayers, numNeurons = self._build_dnn(layer, neuron, activation, dr, lr, lambdaL2, trainNormX)
                                        
                                        history = model.fit(
                                            trainNormX, trainY, epochs=epoch, batch_size=batch, validation_split=0.3, shuffle=False, verbose=2, use_multiprocessing=True, workers=self.cores
                                        )
                                        eTime = time.time()
                                        
                                        predY = model.predict(
                                            testNormX, verbose=2, use_multiprocessing=True, workers=self.cores
                                        )
                                        
                                        observe_training(history, testY, predY, sTime)
                                        
                                        metrics = Metrics(testY, predY)
                                        mape = metrics.MAPE()
                                        rmse = metrics.RMSE()
                                        mae = metrics.MAE()
                                        accuracy = 100 - mape
                                        runTime = round((eTime - sTime) / 60, 2)
                                        
                                        mask = '%Y%m%d_%H%M%S'
                                        dte = time.strftime(mask, time.localtime(sTime))
                                        modelName = '-{}.h5'.format(dte)
                                        
                                        metricsResult = pd.DataFrame(
                                            {
                                                'testtime': [dte],
                                                'runtime': [runTime],
                                                'numlayers': [numLayers],
                                                'numneurons': [numNeurons],
                                                'epoch': [epoch],
                                                'batch': [batch],
                                                'activation': [activation],
                                                'lr': [lr],
                                                'dr': [dr],
                                                'ld': [lambdaL2],
                                                'accuracy': [accuracy],
                                                'mape': [mape],
                                                'rmse': [rmse],
                                                'mae': [mae]
                                            }
                                        )
                                        
                                        print(metricsResult)
                                        save_result(metricsResult, model, modelName)
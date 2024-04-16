import os
import datetime
import logging
import json
import time
import matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import r2_score
from functools import wraps
from joblib import dump, load

matplotlib.use('Agg')


def create_folder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print(f'[ERROR] => Creating Folder Error {dir}')
        
        
def date_generator(startYear, endYear):
    startDate = datetime.date(startYear, 1, 1)
    endDate = datetime.date(endYear, 3, 31)
    
    dateList = []
    
    currentDate = startDate
    
    while currentDate <= endDate:
        dateList.append(currentDate.strftime('%Y%m'))
        currentDate = currentDate.replace(day=1) + datetime.timedelta(days=32)
        currentDate = currentDate.replace(day=1)
         
    return dateList


def scaler_norm(self, data, train_data):
        mean = np.mean(train_data)
        std = np.std(train_data)
        normed_col = (data - mean) / std
        
        return normed_col


def logger(loggerName, logFile, level=logging.INFO):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    
    return logger


def timer(function):
    @wraps(function)
    def measure(*args, **kwargs):
        sTime = time.time()
        result = function(*args, **kwargs)
        eTime = time.time()
        runTime = round((eTime - sTime) / 60, 2)
        print(f'[RUN TIME] => [{function.__name__} Elapsed {runTime} mins]')
        return result, runTime
    return measure

class Metrics:
    def __init__(self, test, pred):
        self.test = test
        self.pred = pred
    
    def MAPE(self):
        mape = round(np.mean(np.abs((self.test - self.pred) / self.test)) * 100, 2)
        mape = mape.values.item()
        return mape

    def MAE(self):    
        mae = round(np.mean(np.abs(self.test - self.pred)), 2)
        mae = mae.values.item()
        return mae
    
    def RMSE(self):
        rmse = round(np.sqrt(np.mean(np.subtract(self.test, self.pred) ** 2)), 2)
        rmse = rmse.values.item()
        return rmse
    
    def MSE(self):
        mse = round(np.mean(np.subtract(self.test, self.pred) ** 2), 2)
        mse = mse.values.item()
        return mse
    
    def R2(self):
        r2 = round(r2_score(self.test, self.pred), 2)
        return r2
    
    
def save_json(configJson, config):
    with open(configJson, 'w') as f:
        json.dump(config, f, indent=4)
    
    
def create_tensorboard_dir(dir_name, sTime):
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    
    root_logdir = os.path.join('./results/dnn/tensorboard', dir_name)
    sub_dir_name = dte
    
    return os.path.join(root_logdir, sub_dir_name)
    
    
def observe_dnn_training(history, test, pred, sTime) :
    loss = history.history['loss']
    valLoss = history.history['val_loss']
    mae = history.history['mae']
    valMae = history.history['val_mae']
    lr = history.history['lr']
    epochs = range(1, len(loss) + 1)
    error = test - pred
    
    _, axes = plt.subplots(3, 2, figsize = (24, 18))
    
    axes[0, 0].plot(epochs, loss, label = 'Training Loss')
    axes[0, 0].plot(epochs, valLoss, label = 'Validation Loss')
    axes[0, 0].set_title('Training and Validation Loss')
    axes[0, 0].legend()
    
    axes[0, 1].plot(epochs, mae, label = 'Training MAE')
    axes[0, 1].plot(epochs, valMae, label = 'Validation MAE')
    axes[0, 1].set_title('Training and Validation MAE')
    axes[0, 1].legend()
    
    axes[1, 0].plot(epochs, lr, label='Learning Rate')
    axes[1, 0].set_title('Diff of Learning Rate')
    
    axes[1, 1].scatter(test, pred)
    axes[1, 1].set_title('Actual and Predicted Price')
    axes[1, 1].set_xlabel('Actual Price')
    axes[1, 1].set_ylabel('Predicted Price')

    axes[2, 0].plot(test, label='Actual')
    axes[2, 0].plot(pred, label='Prediction')
    axes[2, 0].set_title('Actual and Predicted Price')
    axes[2, 0].legend()
    
    axes[2, 1].hist(error)
    axes[2, 1].set_xlabel('Prediction Error')
    axes[2, 1].set_ylabel('Frequency')
    axes[2, 1].set_title('Distribution of Prediction Error')
    
    plt.tight_layout()
    
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    gname = '-{}.png'.format(dte)
    
    create_folder('./figures/observe_dnn_training')
    plt.savefig('./figures/observe_dnn_training/DNN' + gname)
    plt.cla()
    plt.clf()
    plt.close()
    

def observe_reg_training(test, pred, trainLoss, testLoss, sTime) :
    residual = test - pred
    
    _, axes = plt.subplots(2, 2, figsize = (24, 18))
    
    axes[0, 0].scatter(test, pred, color='blue')
    axes[0, 0].set_title('Actual and Predicted Price')
    axes[0, 0].set_xlabel('Actual Price')
    axes[0, 0].set_ylabel('Predicted Price')
    axes[0, 0].grid(True)
    
    axes[0, 1].scatter(pred, residual, color='blue')
    axes[0, 1].set_title('Residual of Prediction Value')
    axes[0, 1].set_xlabel('Predicted Price')
    axes[0, 1].set_ylabel('Residual')
    axes[0, 1].axhline(y=0, color='red', linestyle='--')
    axes[0, 1].grid(True)
    
    axes[1, 0].hist(residual)
    axes[1, 0].set_xlabel('Prediction Error')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Distribution of Prediction Error')
    
    axes[1, 1].plot(trainLoss, label='Training Loss')
    axes[1, 1].plot(testLoss, label='Validataion Loss')
    axes[1, 1].set_title('Regression Learning Curve')
    axes[1, 1].set_xlabel('Length of Training Data')
    axes[1, 1].set_ylabel('MSE')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    gname = '-{}.png'.format(dte)
    
    create_folder('./figures/observe_reg_training')
    plt.savefig('./figures/observe_reg_training/Reg' + gname)
    plt.cla()
    plt.clf()
    plt.close()
        
        
def save_dnn_result(model, numLayers, numNeurons, epoch, batch, activation, lr, dr, lambdaL2, test, pred, accelator, sTime, eTime) :
    create_folder('./results/dnn')
    create_folder('./results/dnn/models')
    
    metrics = Metrics(test, pred)
    mape = metrics.MAPE()
    rmse = metrics.RMSE()
    mae = metrics.MAE()
    accuracy = round((100 - mape), 2)
    runTime = round((eTime - sTime) / 60, 2)
    
    if accelator == '0':
        accelatorName = 'GPU'
    elif accelator == '-1':
        accelatorName = 'CPU'
        
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    modelName = '-{}.h5'.format(dte)
    
    metricsResult = pd.DataFrame(
        {
            'testtime': [dte],
            'accelator': [accelatorName],
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
    
    print('\n\n', metricsResult, '\n\n')
    
    if not os.path.exists('./results/dnn/result.csv'):
        metricsResult.to_csv('./results/dnn/result.csv', mode='w', header=True, index=False)
    else:
        metricsResult.to_csv('./results/dnn/result.csv', mode='a', header=False, index=False)
        
    model.save('./results/dnn/models/DNN' + modelName)
    
    
def save_reg_result(model, test, pred, evalTrain, sTime, eTime) :
    create_folder('./results/reg')
    create_folder('./results/reg/models')
    
    metrics = Metrics(test, pred)
    mape = metrics.MAPE()
    rmse = metrics.RMSE()
    mae = metrics.MAE()
    r2 = metrics.R2()
    accuracy = round((100 - mape), 2)
    runTime = round((eTime - sTime) / 60, 2)
        
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    modelName = '-{}.joblib'.format(dte)
    
    metricsResult = pd.DataFrame(
        {
            'testtime': [dte],
            'runtime': [runTime],
            'r2': [r2],
            'accuracy': [accuracy],
            'mape': [mape],
            'rmse': [rmse],
            'mae': [mae]
        }
    )

    if not os.path.exists('./results/reg/result.csv'):
        metricsResult.to_csv('./results/reg/result.csv', mode='w', header=True, index=False)
    else:
        metricsResult.to_csv('./results/reg/result.csv', mode='a', header=False, index=False)
        
    dump(model, f'./results/reg/models/Reg{modelName}')
    
    print(f'\n\n Train R2 => {evalTrain} \n\n')
    print('\n\n', metricsResult, '\n\n')
    
    
def save_dnn_pretrain_result(pretrainY, predY, sTime) :
    create_folder('./results/dnn/pretrain')
    
    metrics = Metrics(pretrainY, predY)
    mape = metrics.MAPE()
    rmse = metrics.RMSE()
    mae = metrics.MAE()
    r2 = metrics.R2()
    accuracy = round((100 - mape), 2)
    diff = np.round(np.abs(pretrainY.values.flatten() - predY.flatten()), 2)
    diffpercent = np.round(np.abs(pretrainY.values.flatten() - predY.flatten()) / pretrainY.values.flatten() * 100, 2)
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    pretrainValueName = '-{}.csv'.format(dte)
    
    pretrainResult = pd.DataFrame(
        {
            'testtime': [dte],
            'r2': [r2],
            'accuracy': [accuracy],
            'mape': [mape],
            'rmse': [rmse],
            'mae': [mae]
        }
    )
    
    pretrainValue = pd.DataFrame(
        {
            'actual': pretrainY.values.flatten(),
            'pred': np.round(predY.flatten()),
            'diff': diff,
            'diffpercent': diffpercent
        }
    )
    
    print('\n\n', pretrainResult, '\n\n')
    
    if not os.path.exists('./results/dnn/pretrainResult.csv'):
        pretrainResult.to_csv('./results/dnn/pretrainResult.csv', mode='w', header=True, index=False)
    else:
        pretrainResult.to_csv('./results/dnn/pretrainResult.csv', mode='a', header=False, index=False)
        
    # pretrainValue.to_csv('./results/dnn/pretrain/' + pretrainValueName)
    

def save_reg_pretrain_result(pretrainY, predY, sTime) :
    create_folder('./results/reg/pretrain')
    
    metrics = Metrics(pretrainY, predY)
    mape = metrics.MAPE()
    rmse = metrics.RMSE()
    mae = metrics.MAE()
    r2 = metrics.R2()
    accuracy = round((100 - mape), 2)
    diff = np.round(np.abs(pretrainY.values.flatten() - predY.flatten()), 2)
    diffpercent = np.round(np.abs(pretrainY.values.flatten() - predY.flatten()) / pretrainY.values.flatten() * 100, 2)
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(sTime))
    pretrainValueName = '-{}.csv'.format(dte)
    
    pretrainResult = pd.DataFrame(
        {
            'testtime': [dte],
            'r2': [r2],
            'accuracy': [accuracy],
            'mape': [mape],
            'rmse': [rmse],
            'mae': [mae]
        }
    )
    
    pretrainValue = pd.DataFrame(
        {
            'actual': pretrainY.values.flatten(),
            'pred': np.round(predY.flatten()),
            'diff': diff,
            'diffpercent': diffpercent
        }
    )
    
    print('\n\n', pretrainResult, '\n\n')
    
    if not os.path.exists('./results/reg/pretrainResult.csv'):
        pretrainResult.to_csv('./results/reg/pretrainResult.csv', mode='w', header=True, index=False)
    else:
        pretrainResult.to_csv('./results/reg/pretrainResult.csv', mode='a', header=False, index=False)
        
    # pretrainValue.to_csv('./results/dnn/pretrain/' + pretrainValueName)
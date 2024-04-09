import os
import datetime
import logging
import json
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from functools import wraps

matplotlib.use('Agg')

def create_folder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print(f'[ERROR] => Creating Folder Error {dir}')
        
def date_generator(startYear, endYear):
    startDate = datetime.date(startYear, 1, 1)
    endDate = datetime.date(endYear, 12, 31)
    
    dateList = []
    
    currentDate = startDate
    
    while currentDate <= endDate:
        dateList.append(currentDate.strftime('%Y%m'))
        currentDate = currentDate.replace(day=1) + datetime.timedelta(days=32)
        currentDate = currentDate.replace(day=1)
         
    return dateList

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
        mse = round(np.mean(np.substract(self.test, self.pred) ** 2), 2)
        mse = mse.values.item()
        return mse
    
def observe_training(history, test, pred, startTime) :
    loss = history.history['loss']
    valLoss = history.history['val_loss']
    mae = history.history['mae']
    valMae = history.history['val_mae']
    epochs = range(1, len(loss) + 1)
    # error = test - pred
    
    _, axes = plt.subplots(2, 2, figsize = (24, 18))
    
    axes[0, 0].plot(epochs, loss, label = 'Training Loss')
    axes[0, 0].plot(epochs, valLoss, label = 'Validation Loss')
    axes[0, 0].set_title('Training and Validation Loss')
    axes[0, 0].legend()
    
    axes[0, 1].plot(epochs, mae, label = 'Training MAE')
    axes[0, 1].plot(epochs, valMae, label = 'Validation MAE')
    axes[0, 1].set_title('Training and Validation MAE')
    axes[0, 1].legend()
    
    axes[1, 0].scatter(test, pred)
    axes[1, 0].set_title('Actual and Predicted Price')
    axes[1, 0].set_xlabel('Actual Price')
    axes[1, 0].set_ylabel('Predicted Price')

    axes[1, 1].plot(test, label='Actual')
    axes[1, 1].plot(pred, label='Prediction')
    axes[1, 1].set_title('Actual and Predicted Price')
    axes[1, 1].legend()
    
    # axes[2, 0].hist(error)
    # axes[2, 0].set_xlabel('Prediction Error')
    # axes[2, 0].set_ylabel('Frequency')
    # axes[2, 0].set_title('Distribution of Prediction Error')
    
    plt.tight_layout()
    
    mask = '%Y%m%d_%H%M%S'
    dte = time.strftime(mask, time.localtime(startTime))
    gname = '-{}.png'.format(dte)
    
    create_folder('./figures/observe_training')
    plt.savefig('./figures/observe_training/DNN' + gname)
        
def save_result(result, model, saveName) :
    create_folder('./results/dnn')
    create_folder('./results/dnn/models')
    
    if not os.path.exists('./results/dnn/result.csv'):
        result.to_csv('./results/dnn/result.csv', mode='w', header=True, index=False)
    else:
        result.to_csv('./results/dnn/result.csv', mode='a', header=False, index=False)
        
    model.save('./results/dnn/models/DNN' + saveName)

def save_json(configJson, config):
    with open(configJson, 'w') as f:
        json.dump(config, f, indent=4)
import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


from data.crawler import *
from data.query import *
from data.preprocessing import *
from analysis.eda import EDA
from models.dnn import DNN
from models.regression import RegressionModel
from models.lightgbm import LightGBM
from utils.utils import *

def main():
    callCols = 'year, district_en, price_unit, con_year, area, floor, py_unit'
    inputData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade_process', callCols, '700000'), columns=tblTradeProcessTotalCols)
    testData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade_test_process', callCols, '10000'), columns=tblTradeTestProcessTotalCols)
    
    # configDnn = {
    #     'layers': [5],
    #     'neurons': [10],
    #     'activations': ['swish'],
    #     'batchnorm': True,
    #     'drs': [0.3],
    #     'lrs': [0.0001],
    #     'lds': [0.1],
    #     'epochs': [1000],
    #     'batchs': [1024],
    #     'accelator': os.environ.get('CUDA_VISIBLE_DEVICES')
    # }
    # save_json('./configs/configurationDNN.json', config)
    
    # dnn = DNN('./configs/configurationDNN.json', inputData, testData)
    # dnn.run_dnn()
    # dnn.run_pretrain_model()
     
    # reg = RegressionModel(inputData, testData)
    # reg.run_regression()
    
    # configLGBM = {
    #     'lrs': [0.1, 0.25, 0.5, 0.01, 0.025, 0.05, 0.001, 0.0025, 0.005],
    #     'ffs': [0.7, 0.8, 0.9],
    #     'bfs': [0.7, 0.8],
    #     'bqs': [10],
    #     'depths': [1, 10, 20, 30, 40, 50, 60],
    #     'leaves': [10, 20, 30, 40, 50, 60, 70, 80],
    #     'bins': [32, 64, 128, 256],
    #     'iters': [100, 500, 1000, 2500, 5000, 10000, 20000, 30000, 40000, 50000]
    # }
    # save_json('./configs/configurationLGBM.json', configLGBM)
    
    configLGBM = {
        'lrs': [0.1],
        'ffs': [0.7],
        'bfs': [0.8],
        'bqs': [10],
        'depths': [10],
        'leaves': [30],
        'bins': [256],
        'iters': [2500]
    }
    save_json('./configs/configurationLGBM.json', configLGBM)
    
    lgb = LightGBM('./configs/configurationLGBM.json', inputData, testData)
    lgb.run_lightgbm()
    
    
if __name__ == '__main__':
    main()
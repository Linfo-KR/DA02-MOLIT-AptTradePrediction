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
from utils.utils import *

def main():
    callCols = 'year, district_en, price_unit, con_year, area, floor, py_unit'
    inputData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade_process', callCols, '700000'), columns=tblTradeProcessTotalCols)
    testData = pd.DataFrame(import_data('AptTradeDB', 'tbl_trade_test_process', callCols, '10000'), columns=tblTradeTestProcessTotalCols)
    
    # config = {
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
    # save_json('./configs/configuration.json', config)
    
    # dnn = DNN('./configs/configuration.json', inputData, testData)
    # dnn.run_dnn()
    # dnn.run_pretrain_model()
    
    reg = RegressionModel(inputData, testData)
    reg.run_regression()
    
if __name__ == '__main__':
    main()
from data.crawler import *
from data.query import *
from data.preprocessing import *
from analysis.eda import EDA
from models.pricing import DNN
from utils.utils import *

def main():
    inputData = preprocessing('700000')

    config = {
        'layers': [5, 10],
        'neurons': [6, 7],
        'activations': ['swish'],
        'drs': [0.1],
        'lrs': [0.0001, 0.0005],
        'lds': [0.1],
        'epochs': [50, 100],
        'batchs': [16, 32]
    }
    save_json('./configs/configuration.json', config)
    
    dnn = DNN('./configs/configuration.json', inputData)
    dnn.run_dnn()
    
if __name__ == '__main__':
    main()
import os
import time
import json
import graphviz
import warnings

import pandas as pd
import lightgbm as lgb

from data.query import *
from data.load_data import *
from models.cuda import *
from utils.utils import *

warnings.filterwarnings('ignore')


class LightGBM:
    def __init__(self, configs, data, pretrainData):
        self.configs = configs
        self._load_config()
        self.data = data
        self.pretrainData = pretrainData
    
    
    def _load_config(self):
        with open(self.configs, 'r') as f:
            self.config = json.load(f)
            
        self.lrs = self.config.get('lrs')
        self.ffs = self.config.get('ffs')
        self.bfs = self.config.get('bfs')
        self.bqs = self.config.get('bqs')
        self.depths = self.config.get('depths')
        self.leaves = self.config.get('leaves')
        self.bins = self.config.get('bins')
        self.iters = self.config.get('iters')
    
    
    def run_lightgbm(self):
        trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY = load_data(self.data, self.pretrainData)
        for lr in self.lrs:
            for ff in self.ffs:
                for bf in self.bfs:
                    for bq in self.bqs:
                        for depth in self.depths:
                            for leaf in self.leaves:
                                for bin in self.bins:
                                    for iter in self.iters:
                                        params = {
                                            'task': 'train',
                                            'boosting_type': 'gbdt',
                                            'objective': 'regression',
                                            'metric': ['mse', 'rmse'],
                                            'learning_rate': lr,
                                            'feature_fraction': ff,
                                            'bagging_fraction': bf,
                                            'bagging_freq': bq,
                                            'verbose': 2,
                                            "max_depth": depth,
                                            "num_leaves": leaf, 
                                            "max_bin": bin,
                                            "num_iterations": iter,
                                            'early_stopping_rounds': 100,
                                            'num_threads': os.cpu_count()
                                        }
                                        
                                        sTime = time.time()
                                        model = lgb.LGBMRegressor(**params)
                                        model.fit(trainNormX, trainY, eval_set=[(testNormX, testY)], eval_metric='mse')
                                        eTime = time.time()
                                        
                                        predY = pd.DataFrame(model.predict(testNormX, num_iteration=model.best_iteration_), index=testY.index, columns=testY.columns)
                                        save_lgb_result(model, lr, ff, bf, bq, depth, leaf, bin, iter, testY, predY, sTime, eTime)
                                        observe_lgb_training(model, testY, predY, sTime)
                                        
                                        pretrainPredY = pd.DataFrame(model.predict(pretrainNormX), index=pretrainY.index, columns=pretrainY.columns)
                                        save_lgb_pretrain_result(pretrainY, pretrainPredY, sTime)
import multiprocessing
import time
import json
import warnings

import pandas as pd
import tensorflow as tf
import tensorflow.keras.backend as k

from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.regularizers import *
from tensorflow.keras.callbacks import *

from data.query import *
from data.load_data import *
from models.cuda import *
from utils.utils import *

warnings.filterwarnings('ignore')

    
class DNN:
    def __init__(self, configs, data, pretrainData):
        self.configs = configs
        self._load_config()
        self.data = data
        self.pretrainData = pretrainData
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
        self.batchnorm = self.config.get('batchnorm')
        self.epochs = self.config.get('epochs')
        self.batchs = self.config.get('batchs')
        self.accelator = self.config.get('accelator')
    
    
    def _build_dnn(self, layers, neurons, activations, drs, lrs, lds, batchnorm, input_shape):
        strategy = gpu_using()
        
        with strategy.scope():
            unit = 2
            
            k.clear_session()
            
            model = Sequential()
            model.add(Dense(unit ** neurons, input_shape=input_shape))
            
            for layer in range(1, layers + 1):
                if lds != 0:
                    model.add(Dense(unit ** neurons, activation=activations, kernel_regularizer=l2(lds)))
                else:
                    model.add(Dense(unit ** neurons, activation=activations))
                    
                if batchnorm == True:
                    model.add(BatchNormalization())
                else:
                    None
                    
                if drs != 0:
                    model.add(Dropout(rate=drs))
                else:
                    None
                
            model.add(Dense(unit ** 0, activation='linear'))
            
            loss = tf.keras.losses.MeanSquaredError(name='mse')
            optimizer = tf.keras.optimizers.Adam(lr=lrs)
            metrics = tf.keras.metrics.MeanAbsoluteError(name='mae')
            model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
            model.summary()
            
            numLayers = 0
            for layer in model.layers:
                if isinstance(layer, Dense):
                    numLayers += 1
                    
                # for weight in layer.weights:
                #     print(f'Layer : {layer.name}, Parameter : {weight.name}, Data Type : {weight.dtype}')
                    
            numLayers = numLayers - 2
            numNeurons = [layer.units for layer in model.layers if isinstance(layer, Dense)]
            
        return model, numLayers, numNeurons
    
    
    def run_dnn(self):
        trainNormX, testNormX, pretrainNormX, trainY, testY, pretrainY = load_data(self.data, self.pretrainData)
        input_shape = [len(trainNormX.keys())]
        train_ds = (tf.data.Dataset.from_tensor_slices((trainNormX, trainY))).batch(self.batchs[0]).prefetch(tf.data.experimental.AUTOTUNE)
        test_ds = (tf.data.Dataset.from_tensor_slices((testNormX, testY))).batch(self.batchs[0]).prefetch(tf.data.experimental.AUTOTUNE)
        
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
                                        if ld == 0:
                                            lambdaL2 = 0
                                        else:
                                            lambdaL2 = initLd * (weightLd ** ld)
                                                                                    
                                        model, numLayers, numNeurons = self._build_dnn(layer, neuron, activation, dr, lr, lambdaL2, self.batchnorm, input_shape)
                                        
                                        tbLogDir = create_tensorboard_dir('tensorboard_log', sTime)
                                        
                                        callbacks = [
                                            tf.keras.callbacks.TensorBoard(log_dir=tbLogDir),
                                            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-8),
                                            tf.keras.callbacks.EarlyStopping(patience=5),
                                            tf.keras.callbacks.ModelCheckpoint(
                                                filepath='./results/dnn/ckpt/CheckPoint.ckpt',
                                                monitor='val_loss', save_best_only=True, save_weights_only=True, verbose=1
                                            )
                                        ]
                                        
                                        history = model.fit(
                                            train_ds, epochs=epoch, validation_data=test_ds, 
                                            shuffle=False, verbose=2, use_multiprocessing=True, workers=self.cores,
                                            callbacks=callbacks
                                        )                                        
                                        eTime = time.time()
                                                                                
                                        loss, mae = model.evaluate(test_ds, verbose=1)
                                        print(f'\n\n loss => {loss} \n mae => {mae} \n\n')
                                        
                                        predY = model.predict(
                                            test_ds, verbose=0, use_multiprocessing=True, workers=self.cores
                                        )
                                        
                                        observe_dnn_training(history, testY, predY, sTime)
                                        save_dnn_result(model, numLayers, numNeurons, epoch, batch, activation,
                                                    lr, dr, lambdaL2, testY, predY, self.accelator, sTime, eTime)
                                        
                                        pretrainModel = model
                                        pretrainPredY = pretrainModel.predict(pretrainNormX)
                                        save_dnn_pretrain_result(pretrainY, pretrainPredY, sTime)
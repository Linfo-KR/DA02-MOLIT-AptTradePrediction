import os
import tensorflow as tf

def gpu_using():
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    
    gpus = tf.config.experimental.list_physical_devices('GPU')
    
    if len(gpus) > 1:
        strategy = tf.distribute.MirroredStrategy(devices=[f'/device:GPU:{i}' for i in range(len(gpus))], cross_device_ops=tf.distribute.HierarchicalCopyAllReduce())
        print('\n\n Running on Multiple GPUs, Devices Info : ', [gpu.name for gpu in gpus], '\n\n')
    elif len(gpus) == 1 :
        strategy = tf.distribute.get_strategy()
        print('\n\n Running on Single GPU, Device Info : ', gpus[0].name)
        print('\n\n #Accelerators : ', strategy.num_replicas_in_sync, '\n\n')
    else :
        strategy = tf.distribute.get_strategy()
        print('\n\n Running on CPU', '\n\n')
        
    return strategy
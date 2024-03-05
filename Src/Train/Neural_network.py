import sqlite3
import time

import numpy as np
import pandas as pd
import tensorflow as tf

from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping

current_time = str(time.time())
tensorboard = TensorBoard(log_dir='../../Logs/{}'.format(current_time))  # Logs tb
model_checkpoint = ModelCheckpoint('../../Models/{}.h5'.format(current_time), save_best_only=True)  # Save best model
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=0, mode='min')  # Stop training if val_loss does not improve

connect_db = sqlite3.connect('../../Data/dataset.sqlite')
df = pd.read_sql_query('SELECT * FROM dataset', connect_db)


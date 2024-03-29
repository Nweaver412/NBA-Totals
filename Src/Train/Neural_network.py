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

dataset = "dataset_2012-24"
con = sqlite3.connect("../../Data/dataset.sqlite")
data = pd.read_sql_query(f"SELECT * FROM \"{dataset}\"", con, index_col="index")
con.close()

scores = data['Score']
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU', 'OU-Cover'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

x_train = tf.keras.utils.normalize(data, axis=1)
y_train = np.asarray(margin)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, validation_split=0.1, batch_size=32, callbacks=[tensorboard, earlyStopping, mcp_save])

print('Done')
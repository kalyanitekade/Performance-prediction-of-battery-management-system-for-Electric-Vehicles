# -*- coding: utf-8 -*-
"""LSTM_SOC_Paper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h-Rk3gmRFbKgWLAz0YS26MQYXZ2fPWBu
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, max_error
from tensorflow import keras
from tensorflow.keras import layers, models
from keras.callbacks import Callback
# Load the data into a Pandas dataframe
data = pd.read_csv("actual_data_bms.csv")

# Split the data into features (x) and target (y)
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

rmse_values = []
mae_values = []
max_abs_error_values = []

for i in range(3):

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=3)

  # Reshape the training and testing data to have three dimensions
  x_train = x_train.values.reshape(-1, 1, 5)
  x_test = x_test.values.reshape(-1, 1, 5)

  model = Sequential()
  model.add(LSTM(256, activation='selu',
                  return_sequences=True,
                  input_shape=(1,4)))
  model.add(LSTM(256, activation='selu', return_sequences=False))
  model.add(Dense(256, activation='selu'))
  model.add(Dense(128, activation='selu'))
  model.add(Dense(1, activation='linear'))
  # Set compile parameters
  epochs = 50
  learn_rate_drop_period = 1000
  initial_learn_rate = 0.01
  learn_rate_drop_factor = 0.1
  validation_frequency = 1

  # Compile the model with mean squared error loss and additional parameters
  lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
      initial_learn_rate, decay_steps=learn_rate_drop_period, decay_rate=learn_rate_drop_factor
  )
  model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
                loss='mean_squared_error')
# Train the model on the training data
  history = model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test, y_test))

  # Evaluate the model on the test data
  test_loss= model.evaluate(x_test, y_test, verbose=0)

  # Evaluate the model on the test data
  train_loss= model.evaluate(x_train, y_train, verbose=0)

  # Make predictions on the test data
  y_pred = model.predict(x_test)
  # Calculate the root mean squared error percentage (RMSE%)
  rmse_percentage = np.sqrt(mean_squared_error(y_test, y_pred)) * 100

  # Calculate the mean absolute error percentage (MAE%)
  mae_percentage = mean_absolute_error(y_test, y_pred) * 100

  # Calculate the maximum absolute error percentage (max error%)
  max_abs_error_percentage = max_error(y_test, y_pred)* 100

  rmse_values.append(rmse_percentage)
  mae_values.append(mae_percentage)
  max_abs_error_values.append(max_abs_error_percentage)

    # Print the accuracy metrics
  print("Test Loss:", test_loss)
  print("Train Loss:", train_loss)
  print("RMSE:", rmse_percentage)
  print("MAE:", mae_percentage)
  print("Max Absolute Error:", max_abs_error_percentage)

import matplotlib.pyplot as plt
plt.figure(figsize=(14, 8))
# Plot the loss values for training and validation sets
plt.plot(range(1, len(history.history['loss']) + 1), history.history['loss'])
plt.plot(range(1, len(history.history['val_loss']) + 1), history.history['val_loss'])

# Set the title, x-axis and y-axis labels, and legend
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Training Loss', 'Validation Loss'], loc='upper right')

# Set the x-axis ticks to integer values
plt.xticks(range(1, len(history.history['loss']) + 1))

# Display the plot
plt.show()

test_labels_vertical = pd.Series(np.ravel(y_test))
test_labels_vertical = test_labels_vertical.values.reshape(-1, 1)
test_labels_vertical = np.around(test_labels_vertical, decimals=2)
print(test_labels_vertical)
print(test_labels_vertical)
len(test_labels_vertical)

test_predictions_vertical = y_pred.reshape(len(y_pred),1)
test_predictions_vertical  = np.around(test_predictions_vertical , decimals=2)
print(test_predictions_vertical)
len(test_predictions_vertical)

true_pred = np.concatenate((test_labels_vertical,test_predictions_vertical),axis=1)
true_pred = np.around(true_pred, decimals=2)
print(true_pred)

import matplotlib.pyplot as plt
plt.scatter(test_labels_vertical, test_predictions_vertical, c='red', label='Predicted SOC')
plt.scatter(test_labels_vertical, test_labels_vertical, c='blue', label='Ideal SOC')
plt.xlabel('Actual SOC from dataset')
plt.xlim(left=0.1, right=1.1)
plt.ylabel('Predicted SOC by model')
plt.ylim(bottom=0.1, top=1.1)
plt.title('Scatter Plot of test and predicted soc')
plt.legend(loc='upper left')
plt.show()

import matplotlib.pyplot as plt

# Plot the Root mean square error (RMSE)
plt.bar(range(1,4), rmse_values, label='RMSE', color='#c7b8e2',width=0.3)
plt.legend()
# Set the x-axis ticks to integer values
plt.xticks(range(1, 4))
plt.xlabel('Iterations')
plt.ylabel('Error %')
plt.title('Root mean square error')
plt.show()

# Plot the Mean Absolute error (MAE)

plt.bar(range(1,4), mae_values, label='MAE', color='#F0E68C',width=0.3)
plt.legend()
# Set the x-axis ticks to integer values
plt.xticks(range(1, 4))
plt.xlabel('Iterations')
plt.ylabel('Error %')
plt.title('Mean Absolute Error')
plt.show()

# Plot the Maximum Absolute Error (MAX)
import matplotlib.pyplot as plt
plt.bar(range(1,4), max_abs_error_values, label='Max Abs Error', color='pink',width=0.3)
plt.legend()
# Set the x-axis ticks to integer values
plt.xticks(range(1, 4))
plt.xlabel('Iterations')
plt.ylabel('Error %')
plt.title('Maximum Absolute Error')
plt.show()

model.summary()
import numpy as np
import pandas as pd
import os

df = pd.read_csv('/Users/mac/Documents/Datasets/Fake News/train.csv')
df.head()
df.info()
df.describe()
#droping any null value
df = df.dropna()

#getting the independent features
X = df.iloc[:,:-1]
print(X)

H = df.drop('label',axis = 1)
print(H)
y = df['label']
print(y)

print('shape of X',X.shape)
print('shape of y',y.shape)

#importing Tensorflow
import tensorflow as tf
tf.__version__

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense

##vocabulary size
vocab_size = 5000

#one_hot representation
messages = X.copy()

messages.reset_index(inplace = True)
messages.title

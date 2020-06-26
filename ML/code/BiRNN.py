import tensorflow as tf
from tensorflow.keras import Model, layers
from tensorflow import keras
import numpy as np

# MNIST dataset parameters
num_classes = 10 # total classses
num_features = 784 # 28*28

#Training Parameters
learning_rate = 0.001
training_steps = 1000
batch_size = 32
display_step = 100

# Network Parameters
# MNIST image shape in 28*28, we will handle 28 sequences of 28 timesteps for each sample
num_input = 28
timesteps = 28
num_units = 32 # number of neurons for LSTM layer

(x_train, y_train),(x_test, y_test) = keras.datasets.mnist.load_data()
x_train, x_test = np.array(x_train, np.float32), np.array(x_test, np.float32)
print(x_train.shape, x_test.shape)
# x_train = x_train.reshape((-1, 28, 28))
x_train, x_test = x_train / 255., x_test / 255.
db_train = tf.data.Dataset.from_tensor_slices((x_train, x_test))
db_train = db_train.shuffle(100).batch(batch_size, drop_remainder=True)

class BiRNN(Model):
    def __init__(self):
        super(BiRNN, self).__init__()
        lstm_fw = layers.LSTM(units=num_units)
        lstm_bw = layers.LSTM(units=num_units, go_backwards=True)
        # BiRNN layer
        self.bi_lstm = layers.Bidirectional(lstm_fw, backward_layer=lstm_bw)
        # output layer(num_classes)
        self.out = layers.Dense(num_classes)
    # TODO




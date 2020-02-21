import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras

cell = layers.SimpleRNNCell(3)
cell.build(input_shape=(None, 4))
# print(cell.trainable_variables)

x = tf.random.normal(shape=(4, 80, 100))
xt0 = x[:, 0, :]
cell = layers.SimpleRNNCell(64)
out, ht1 = cell(xt0, [tf.zeros(shape=(4, 64))])

# print(out.shape, ht1[0].shape)

cell = layers.SimpleRNNCell(64)
cell2 = layers.SimpleRNNCell(64)
state0 = [tf.zeros(shape=(4, 64))]
state1 = [tf.zeros(shape=(4, 64))]

out0, state0 = cell(xt0, state0)
out1, state1 = cell2(out0, state1)

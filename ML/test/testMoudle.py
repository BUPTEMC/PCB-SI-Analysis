import tensorflow as tf
import numpy as np

a = tf.convert_to_tensor([[1,1,1,3],[0,4,0,1]])
mask = tf.math.logical_not(tf.math.equal(a, 0))
# print(mask)

test = tf.random.normal(shape=(5, 80, 100))
ll = tf.expand_dims(test[:, 1], 1)
print(ll.shape)

a = [1,2,3] + [[0,0,0],[1,1,1]]
b = [1,2,3,[1,1,1],[2,2,2]]
c = zip(a,b)
print(list(c))

bb = tf.convert_to_tensor([[0.334, 0.666]])
print(tf.argmax(bb[0]).numpy())

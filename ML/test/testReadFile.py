import pandas as pd
import tensorflow as tf

input_data = pd.read_csv("../output/demo2.csv", header=None)
# print(input_data.shape)
input_data = tf.convert_to_tensor(input_data.values)
print(input_data[1])

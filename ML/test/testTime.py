from code import RNNSeq2Seq as R
import tensorflow as tf
import pandas as pd
import time
# input_data = pd.read_csv("../output/SampleAD-01.csv", header=None)
input_data = pd.read_csv("../output/AD8367_VGA.csv")
# print(input_data.head(5))
input_data = tf.convert_to_tensor(input_data.values)
print(input_data.shape)
# input_data = tf.expand_dims(input_data, axis=0)
# print(input_data.shape)

# encoder = R.Encoder(1, 1024)
# o, hidden = encoder.call(input_data, encoder.initialize_hidden_state())
# print(o.shape)
# print(input_data)
begin = time.time()
result = R.evaluate(input_data)
end = time.time()
print(result)
print('time:', end - begin)

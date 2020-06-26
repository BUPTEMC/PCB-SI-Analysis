import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import os
import sys
import time
import tensorflow as tf
from tensorflow import keras

print(tf.__version__)
print(sys.version_info)
for module in mpl, np, pd, sklearn, tf, keras:
    print(module.__name__, module.__version__)

# 1. preprocessing data
# 2. build model
# 2.1 encoder
# 2.2 attention
# 2.3 decoder
# 3. evaluation
# 3.1 give data, return result
# 3.2 visualize


encoding_units = 1024
batch_size = 1
classify = {0: 'ok', 1: 'crosstalked'}


class Encoder(keras.Model):
    def __init__(self, batch_size, encoding_units):
        super(Encoder, self).__init__()
        self.batch_size = batch_size
        self.encoding_units = encoding_units
        self.gru = keras.layers.GRU(self.encoding_units,
                                    return_sequences=True,
                                    return_state=True,
                                    recurrent_initializer='glorot_uniform')

    def call(self, inputs, hidden):
        x = inputs
        output, state = self.gru(x, initial_state=hidden)
        return output, state

    def initialize_hidden_state(self):
        return tf.zeros((self.batch_size, self.encoding_units))


encoder = Encoder(batch_size, encoding_units)
sample_hidden = encoder.initialize_hidden_state()
x = tf.random.normal(shape=(1, 80, 256))
# output, sample_hidden = encoder.call(x, sample_hidden)
# print("output shape: ", output.shape)
# print("state shape: ", sample_hidden.shape)


class BahdanauAttention(keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = keras.layers.Dense(units)
        self.W2 = keras.layers.Dense(units)
        self.V = keras.layers.Dense(1)

    def call(self, decoder_hidden, encoder_outputs):
        # decoder_hidden: [b, units]
        # encoder_outputs: [b, len, units]
        # [b, units] -> [b, 1, units]
        decoder_hidden_with_time_axis = tf.expand_dims(decoder_hidden, 1)

        # [b, len, units] -> [b, len, 1]
        score = self.V(
            tf.nn.tanh(
                self.W1(encoder_outputs) + self.W2(decoder_hidden_with_time_axis)))
        # shape: [b, len, 1]
        attention_weights = tf.nn.softmax(score, axis=1)

        # [b, len, 1] -> [b, len, output_units]
        context_vector = attention_weights * encoder_outputs

        # [b, len, output_units] -> [b, output_units]
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


attention_model = BahdanauAttention(units=1024)
# attention_results, attention_weights = attention_model.call(sample_hidden, output)
# print("attention_results: ", attention_results.shape)
# print("attention_weights: ", attention_weights.shape)


class Decoder(keras.Model):
    def __init__(self, batch_size, decoding_units, classifies):
        super(Decoder, self).__init__()
        self.batch_size = batch_size
        self.decoding_units = decoding_units
        self.gru = keras.layers.GRU(self.decoding_units,
                                    return_sequences=True,
                                    return_state=True,
                                    recurrent_initializer='glorot_uniform')
        self.fc = keras.layers.Dense(classifies)
        self.attention = BahdanauAttention(self.decoding_units)

    def call(self, inputs, hidden, encoding_outputs):
        # [b, 1, embedding_units]： single step decoder
        x = tf.cast(inputs, dtype=tf.float32)

        # context_vector: [b, units]
        context_vector, attention_weights = self.attention(
            hidden, encoding_outputs
        )

        # [b, 1, 2*units]
        combined_x = tf.concat(
            [tf.expand_dims(context_vector, axis=1), x], axis=-1
        )

        # output shape: [b, 1, decoding_units]
        # state shape: [b, decoding_units]
        output, state = self.gru(combined_x)

        # [b, 1, decoding_units] -> [b, decoding_units]
        output = tf.reshape(output, shape=(-1, output.shape[2]))

        # [b, classifies]
        predictions = self.fc(output)

        return predictions, state, attention_weights


decoder = Decoder(batch_size, encoding_units, 2)

optimizer = keras.optimizers.Adam(0.001)

loss_object = keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none'
)

def loss_function(real, pred):
    # TODO：以下代码用于去除padding，因为每个PCB板SI结构肯定不一样多
    mask = tf.math.logical_not(tf.math.equal(real, -1))
    loss_ = loss_object(real, pred)
    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask

    return tf.reduce_mean(loss_)


def train_step(inp, targ, encoding_hidden):
    # inp: [b, len, embedding_units]
    # targ: [b, len, classifies]
    loss = 0
    with tf.GradientTape() as tape:
        encoding_outputs, encoding_hidden = encoder(inp, encoding_hidden)
        decoding_hidden = encoding_hidden

        # every SI model's prediction should calculate losses
        for t in range(0, inp.shape[1] - 1):
            # use original inp to predict
            decoding_input = tf.expand_dims(inp[:, t], 1)

            predictions, decoding_hidden = decoder.call(decoding_input, decoding_hidden, encoding_outputs)
            loss += loss_function(targ[:, t], predictions)

    batch_loss = loss / int(targ.shape[0])
    variables = encoder.trainable_variables + decoder.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))
    return batch_loss

def evaluate(input_data):
    result = []
    # attention_matrix = np.zeros()
    # encoding_hidden = encoder.initialize_hidden_state()
    encoding_hidden = tf.random.normal((1, encoding_units))
    _inputs = tf.expand_dims(input_data, axis=0)
    encoding_outputs, encoding_hidden = encoder(_inputs, encoding_hidden)
    print("encoding_outputs:", encoding_outputs.shape)
    print("encoding_hidden:", encoding_hidden.shape)
    decoding_hidden = encoding_hidden
    decoding_input = tf.zeros((1, 1, input_data.shape[1]))
    print("decoding_input:", decoding_input.shape)
    for t in range(input_data.shape[0]):
        pre, decoding_hidden, attention_weights = decoder.call(decoding_input, decoding_hidden, encoding_outputs)
        # attention_weights = tf.reshape(attention_weights, (-1, ))
        # attention_matrix[t] =  attention_weights.numpy()

        predicted_id = tf.argmax(pre[0]).numpy()
        result.append(classify.get(predicted_id))
        decoding_input = tf.expand_dims(tf.expand_dims(input_data[t], axis=0), axis = 0)
    return result


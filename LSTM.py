import numpy as np
import tensorflow as tf

n_steps = 20
n_inputs = 102
n_neurons = 50
n_outputs = 102
learning_rate = 0.001

X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
Y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])

cell = tf.contrib.rnn.OutputProjectionWrapper(
    tf.contrib.rnn.BasicLSTMCell(num_units=n_neurons, activation=tf.nn.leaky_relu),
    output_size=n_outputs
)

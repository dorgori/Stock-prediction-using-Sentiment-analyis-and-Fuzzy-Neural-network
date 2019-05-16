from __future__ import print_function
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('PATH/', one_hot=True)    #one_hot = formating data that more machine readable

#hyperparameters
learning_rate = 0.001
training_iters = 200000
batch_size = 128
display_step = 10

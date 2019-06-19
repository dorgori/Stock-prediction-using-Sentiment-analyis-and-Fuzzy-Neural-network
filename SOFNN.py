import tensorflow as tf
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
from keras.models import Model, clone_model
from keras.layers import Input, Dense



# inputs
open_list = [202.830002, 204.429993, 207.360001]
close_list = [204.529999, 207.479996, 207.160004]
high_list = [204.940002, 207.75, 208.479996]
low_list = [202.339996, 203.899994, 207.050003]
joy_list = [0.229085423, 0.168534917, 0.217908807]
sup_list = [0.149770729, 0.118387816, 0.127869071]
mood_list = joy_list + sup_list

var = np.var(open_list)
print(var)
mean = np.mean(open_list)**2
print(mean)
#gauasian = np.exp(-(open_list[0] - mean)/var)
#print(gauasian)
# calculate Mik
# normalize Mik
list = []
list.append(open_list[0])
list.append(close_list[0])
list.append(high_list[0])
list.append(low_list[0])
list.append(mood_list[0])

num_classes = 5
net = tf.reshape(net, list)
net = tf.layers.dense(inputs=list, name ='layer1',
                      units=5, activation=None)


print('open: ')
print(open_list)
print('close: ')
print(close_list)
print('high: ')
print(high_list)
print('low: ')
print(low_list)
print('mood: ')
print(mood_list)

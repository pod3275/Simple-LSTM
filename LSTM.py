# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 20:19:44 2018

@author: lawle
"""

import csv
import numpy as np
import tensorflow as tf

n_step = 5
n_input = n_class = 102
n_hidden = 128
start_learning_rate = 0.001
total_epoch = 10
batch_size = 256

menu_arr = []
train_data = []
validation_data = []
test_data = []


# menu vocab 만들기
with open('menu_list.csv', mode='r', encoding='utf-8') as r_file:
    reader = csv.reader(r_file)
    for row in reader:
        menu_arr = row
    r_file.close()
            
num_dic = {n: i for i,n in enumerate(menu_arr)}
dic_len = len(num_dic)


# training, validation, test data 로드
with open('training_data.csv', mode='r', encoding='utf-8') as train_file:
    reader = csv.reader(train_file)
    for row in reader:
        train_data.append(row)
    train_file.close()
    
with open('test_data.csv', mode='r', encoding='utf-8') as test_file:
    reader = csv.reader(test_file)
    for row in reader:
        test_data.append(row)
    test_file.close()
    
with open('validation_data.csv', mode='r', encoding='utf-8') as validation_file:
    reader = csv.reader(validation_file)
    for row in reader:
        validation_data.append(row)
    validation_file.close()
    
# mini batch 구성
def make_batch(batch_index, batch_size):
    input_batch = []
    target_batch = []
        
    for i in range(batch_index*batch_size, min((batch_index+1)*batch_size, len(train_data))):
        input = [num_dic[n] for n in train_data[i][:-1]]
        target = num_dic[train_data[i][-1]]
        input_batch.append(np.eye(dic_len)[input])
        target_batch.append(target)
        
    return input_batch, target_batch


def make_test_batch(data):
    input_batch = []
    target_batch = []
    
    for i in range(len(validation_data)):
        input = [num_dic[n] for n in validation_data[i][:-1]]
        target = num_dic[validation_data[i][-1]]
        input_batch.append(np.eye(dic_len)[input])
        target_batch.append(target)
        
    return input_batch, target_batch
    

X = tf.placeholder(tf.float32, [None, n_step, n_input])
Y = tf.placeholder(tf.int32, [None])
dropout_rate = tf.placeholder(tf.float32)

with tf.name_scope('cell1'):
    W = tf.Variable(tf.random_normal([n_hidden, n_class]), name='W1')
    b = tf.Variable(tf.random_normal([n_class]))
    
global_step = tf.Variable(0, trainable=False)

cell1 = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_hidden)
cell2 = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_hidden)
cell3 = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_hidden)

multi_cell = tf.nn.rnn_cell.MultiRNNCell([cell1, cell2, cell3])
multi_cell = tf.nn.rnn_cell.DropoutWrapper(multi_cell, output_keep_prob=dropout_rate)

outputs, states = tf.nn.dynamic_rnn(multi_cell, X, dtype=tf.float32)

outputs = tf.transpose(outputs, [1,0,2])
outputs = outputs[-1]
model = tf.matmul(outputs, W) + b

with tf.name_scope('optimizer'):
    cost = tf.reduce_mean(
            tf.nn.sparse_softmax_cross_entropy_with_logits(
                    logits=model, labels=Y))
    
    prediction = tf.cast(tf.argmax(model, 1), tf.int32)
    prediction_check = tf.equal(prediction, Y)
    accuracy = tf.reduce_mean(tf.cast(prediction_check, tf.float32))
    
    learning_rate = tf.train.exponential_decay(start_learning_rate, global_step, 100000, 0.96, staircase=True)
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost, global_step=global_step)
    tf.summary.scalar('cost', cost)
    tf.summary.scalar('accuracy', accuracy)
    

sess = tf.Session()
sess.run(tf.global_variables_initializer())

total_batch = int(np.ceil(len(train_data) / batch_size))

merged = tf.summary.merge_all()
writer = tf.summary.FileWriter('./logs', sess.graph)

for epoch in range(total_epoch):
    
    for batch_index in range(total_batch):
        X_batch, y_batch = make_batch(batch_index, batch_size)
        _, loss = sess.run([optimizer, cost], 
                           feed_dict={X: X_batch, Y: y_batch, dropout_rate: 0.75})
        
        _, acc = sess.run([prediction, accuracy], 
                           feed_dict={X: X_batch, Y: y_batch, dropout_rate: 1.0})
                
        if ((epoch*total_batch+batch_index+1)%100 == 0):
            print('Iteration:', '%04d' % (epoch*total_batch+batch_index + 1),
                  'Accuracy =', '{:.6f}'.format(acc))
            
        summary = sess.run(merged, feed_dict={X: X_batch, Y: y_batch, dropout_rate: 1.0})
        writer.add_summary(summary, global_step = sess.run(global_step))

print('End.')

test_input, test_output = make_test_batch(validation_data)
predict, accuracy_val = sess.run([prediction, accuracy],
                                 feed_dict={X: test_input, Y: test_output, dropout_rate: 1.0})

print('\n=== 예측 결과 ===')
print('정확도:',accuracy_val*100)

        
        
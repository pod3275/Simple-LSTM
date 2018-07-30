# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:11:00 2018

@author: lawle
"""

import csv
import numpy as np

train_rate = 0.8
validation_rate = 0.1
test_rate = 0.1

menu_arr = []
data = []
training = []
test = []
validation = []


with open('menu_list.csv', mode='r', encoding='utf-8') as r_file:
    reader = csv.reader(r_file)
    for row in reader:
        menu_arr = row
    r_file.close()
    
with open('create_data.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    for row in reader:
        data.append(row)
    
    read_file.close()
    
    
data_split = {A:[] for A in menu_arr}
training_split = {A:[] for A in menu_arr}
validation_split = {A:[] for A in menu_arr}
test_split = {A:[] for A in menu_arr}


for i in range(len(data)):
    for j in menu_arr:
        if data[i][5] == j:
            data_split[j].append(i)


for j in menu_arr:
    train_num = (int)(len(data_split[j])*train_rate)
    test_num = train_num + (int)(len(data_split[j])*test_rate)
    training_split[j] = data_split[j][0:train_num]
    validation_split[j] = data_split[j][train_num:test_num]
    test_split[j] = data_split[j][test_num:len(data_split[j])]


for j in menu_arr:
    for i in training_split[j]:
        training.append(data[i])
    for i in validation_split[j]:
        validation.append(data[i])
    for i in test_split[j]:
        test.append(data[i])


np.random.shuffle(training)
np.random.shuffle(test)
np.random.shuffle(validation)


with open('training_data.csv', mode='w', encoding='utf-8', newline='') as train_write:
    writer = csv.writer(train_write)
    for row in training:
        writer.writerow(row)
    train_write.close()
    
with open('validation_data.csv', mode='w', encoding='utf-8', newline='') as validation_write:
    writer = csv.writer(validation_write)
    for row in validation:
        writer.writerow(row)
    validation_write.close()
    
with open('test_data.csv', mode='w', encoding='utf-8', newline='') as test_write:
    writer = csv.writer(test_write)
    for row in test:
        writer.writerow(row)
    test_write.close()
    

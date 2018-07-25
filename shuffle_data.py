# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:07:37 2018

@author: lawle
"""

import csv
import numpy as np

train_validation_test_rate = 0.8

data = []
training = []
test = []
validation = []

with open('create_data.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    for row in reader:
        data.append(row)
    
    np.random.shuffle(data)
        
    train_num = (int) (len(data)*train_validation_test_rate)
    validation_num = (int) (len(data)*0.1)
    
    training = data[0:train_num]
    
    validation = data[train_num:train_num+validation_num]
        
    test = data[train_num+validation_num:len(data)]
    
    with open('training_data.csv', mode='w', encoding='utf-8', newline='') as train_write:
        writer1 = csv.writer(train_write)
        for row in training:
            writer1.writerow(row)
        train_write.close()
    
    with open('validation_data.csv', mode='w', encoding='utf-8', newline='') as validation_write:
        writer3 = csv.writer(validation_write)
        for row in validation:
            writer3.writerow(row)
        validation_write.close()
    
    with open('test_data.csv', mode='w', encoding='utf-8', newline='') as test_write:
        writer2 = csv.writer(test_write)
        for row in test:
            writer2.writerow(row)
        test_write.close()
        
    read_file.close()
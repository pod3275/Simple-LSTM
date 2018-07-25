# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:26:43 2018

@author: lawle
"""

from dateutil.parser import parse
import csv

data = []

with open('use_log_no_duplicate.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    next(reader)
    
    for row in reader:
        data.append(row)
                    
    with open("create_data.csv", mode='w', encoding='utf-8', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',')
        
        for i in range(len(data)):
            if i>=5:
                if (data[i-5][1] == data[i-4][1] and data[i-4][1] == data[i-3][1] and data[i-3][1] == data[i-2][1] and 
                    data[i-2][1] == data[i-1][1] and data[i-1][1] == data[i][1] and 
                    parse(data[i-5][0]).day == parse(data[i-4][0]).day and parse(data[i-4][0]).day == parse(data[i-3][0]).day and 
                    parse(data[i-3][0]).day == parse(data[i-2][0]).day and parse(data[i-2][0]).day == parse(data[i-1][0]).day and 
                    parse(data[i-1][0]).day == parse(data[i][0]).day):
                    
                    writer.writerow([data[i-5][6], data[i-4][6], data[i-3][6], data[i-2][6],data[i-1][6], data[i][6]])
                    
                    if i%100 == 0:
                        print(i)
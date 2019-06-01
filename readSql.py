
import time
import csv, traceback, os

file_name = "C:\\Users\Dor\\Desktop\\data_base.txt"
f = open(file_name,'r',encoding='utf-8')
csvData = ['Date', 'Tweet']

first_date = "2018-06-07.csv"
with open(first_date, 'a', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(csvData)
    for line in f:
        if line != "" and line != '\n':
            data = line.split("\"")
            row = []
            row.append(data[3])
            row.append(str(data[13]))
            writer.writerow(row)

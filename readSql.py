

file_name = "data_base.txt"
f = open(file_name,'r',encoding='utf-8')

for line in f:
    data = line.split("\"")
    data = data[3]
    text = data[13]
    print(text)

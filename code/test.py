# edited by Jin in 2017.10.16

import csv

input_csvFile = open("../rawData/raw_data.csv", "r")
input_reader = csv.reader(input_csvFile)

#record is the array combined by middle type id and sales amount
record = {}
index = 0
for item in input_reader:
    record[index] = []
    record[index].append(item[3])
    record[index].append(item[14])
    index = index + 1

# print(record)

input_csvFile.close()


output_csvFile = open("../rawData/sample_output.csv", "r")
output_reader = csv.reader(output_csvFile)

#fetch the list of types in output file
item_list = []
large_type_list = []
middle_type_list =[]
for line in output_reader:
    if output_reader.line_num == 1:
        continue
    flag = 0
    index2 = 0
    for item in item_list:
        if line[0] == item_list[index2]:
            flag = 1
            break
        index2 = index2 + 1        
    if(flag == 0):
        if(len(line[0]) > 2):
            middle_type_list.append(line[0])
        else:
            large_type_list.append(line[0])
        item_list.append(line[0])

# print(large_type_list,middle_type_list)

sales_amount ={}
for item in middle_type_list:
    sales_amount[item] = 0
# for 
# print(sales_amount)

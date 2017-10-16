# edited by Jin in 2017.10.16

import csv

input_csvFile = open("../rawData/raw_data.csv", "r")
input_reader = csv.reader(input_csvFile)

#result is the dictionary combined by middle type id and sales amount
result = {}
index = 0
for item in input_reader:
    result[index] = []
    result[index].append(item[3])
    result[index].append(item[14])
    index = index + 1

print(result)

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

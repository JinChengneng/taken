import csv

input_csvFile = open("./weekAverage2.csv", "r",encoding = 'utf-8')
input_reader = csv.reader(input_csvFile)

weekAverage = {}

for item in input_reader:
    if input_reader.line_num == 1:
        continue
    key = item[0] + '-'+ item[1]
    weekAverage[key] = item[2]
    
#print(weekAverage)

input_csvFile = open("./salesamount.csv", "r",encoding = 'utf-8')
input_reader = csv.reader(input_csvFile)

modifiedData = []

for item in input_reader:
    if input_reader.line_num == 1:
        continue
    if(item[1]=='20150204'):
        key = item[0] +'-' + '3'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150214'):
        key = item[0] + '-' + '6'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150217'):
        key = item[0] +'-' + '2'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150218'):
        key = item[0] + '-' + '3'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150219'):
        key = item[0] + '-' + '4'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150220'):
        key = item[0]+ '-' + '5'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150221'):
        key = item[0]+ '-' + '6'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150222'):
        key = item[0]+ '-' + '7'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150223'):
        key = item[0]+ '-' + '1'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150224'):
        key = item[0]+ '-' + '2'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150225'):
        key = item[0]+ '-' + '3'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150226'):
        key = item[0]+ '-' + '4'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150331'):
        key = item[0] + '-' + '2'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150409'):
        key = item[0]+ '-' + '4'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    elif(item[1]=='20150416'):
        key = item[0] + '-' + '4'
        item[2] = weekAverage[key]
        modifiedData.append(item)
    else:
        modifiedData.append(item)

# print(modifiedData)
for item in modifiedData:
    print (item[0]+','+item[1]+','+item[2])
        

    
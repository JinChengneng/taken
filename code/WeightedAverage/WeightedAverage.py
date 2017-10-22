import csv,os,sys
#import matplotlib.pyplot as plt
import math

#将日期字符串转换成距离2015年1月1日的天数
def dateTransformToNum(date):
    if(len(date)!=8):
        exit("数据格式错误！")
    month = int(date[4:6])
    date_ = int(date[6:8])
    if(month == 1):
        return date_
    elif(month == 2):
        if(date_<14):
            return 31+date_
        elif(date_>14):
            return 30+date_
        else:
            exit("不存在记录的日期！")
    elif(month==3):
        if(date_==31):
            exit("不存在记录的日期！")
        return 58+date_
    elif(month==4):
        if(date_<9):
            return 88+date_
        elif(date_>9 and date_<16):
            return 87+date_
        elif(date_>16):
            return 86+date_
        else:
            exit("不存在记录的日期！")
    elif(month == 5):
        return 116+date_
# 将距离2015年1月1日的天数转换成日期字符串
def dateTransferToString(date):
    if(date<=0):
        exit("日期不能为负值！")
    elif(date<=31):
        return "201501%02d" % date
    elif(date<=44):
        return "201502%02d" % (date-31)
    elif(date<=58):
        return "201502%02d" % (date-30)
    elif(date<=88):
        return "201503%02d" % (date-58)
    elif(date<=96):
        return "201504%02d" % (date-88)
    elif(date<=102):
        return "201504%02d" % (date-87)
    elif(date<=116):
        return "201504%02d" % (date-86)
    else:
        return "201505%02d" % (date-116)

#生成数据结构productList，表示中类商品随时间的销量
#返回的productList结构为{大类id：[大类名，{中类id：[中类名，{日期：销量}]}]}
def traceProduct(csvfile):
    csv_reader = csv.reader(open(csvfile))
    productList = {}
    for row in csv_reader:
        if(csv_reader.line_num==1):
            continue
        date = dateTransformToNum(row[7])
        wTypeid = row[1]
        wTypeName = row[2]
        mTypeid = row[3]
        mTypeName = row[4]
        if(wTypeid not in productList):
            productList[wTypeid] = [wTypeName,{mTypeid:[mTypeName,{date:1}]}]
        elif(mTypeid not in productList[wTypeid][1]):
            productList[wTypeid][1][mTypeid] = [mTypeName,{date:1}]
        elif(date not in productList[wTypeid][1][mTypeid][1]):
            productList[wTypeid][1][mTypeid][1][date] = 1
        else:
            productList[wTypeid][1][mTypeid][1][date]+=1
    return productList
#将productList输出成文件
def printProductList(productList):
    for wTypeid in productList.keys():
        if(os.path.exists(sys.path[0] + "\\"+wTypeid+productList[wTypeid][0])):
            continue
        os.makedirs(sys.path[0] + "\\"+wTypeid+productList[wTypeid][0])
    for wTypeid in productList.keys():
        path = sys.path[0]+"\\"+wTypeid+productList[wTypeid][0]
        for mTypeid in productList[wTypeid][1].keys():
            mTypeName = productList[wTypeid][1][mTypeid][0]
            mTypeName = mTypeName.replace("/","")
            date_and_salesamount = productList[wTypeid][1][mTypeid][1]
            file = open(path+"\\"+mTypeid+mTypeName,"w")
            for date in date_and_salesamount.keys():
                file.write(str(date)+","+str(date_and_salesamount[date])+"\n")
            file.close()
#以四月份数据生成验证集文件"validate_data"
def createValidateData(productList):
    validateFile = open("validate_data","w")
    validateFile.write("编码,日期,销量\n")
    wTypeAmount = {}
    for wTypeid in sorted(productList):
        wTypeAmount[wTypeid]={}
        sorted_mid = sorted(productList[wTypeid][1])
        for mTypeid in sorted_mid:
            date_and_salesamount = productList[wTypeid][1][mTypeid][1]
            date_ = sorted(date_and_salesamount)
            a = 1+1
            for date in date_:
                string_date = dateTransferToString(date)
                month = string_date[4:6]
                if(month!="04"):
                    continue
                validateFile.write(mTypeid+","+string_date+
                                       ","+str(date_and_salesamount[date])+"\n")
                if(string_date not in wTypeAmount[wTypeid]):
                    wTypeAmount[wTypeid][string_date]=date_and_salesamount[date]
                else:
                    wTypeAmount[wTypeid][string_date] += date_and_salesamount[date]
    sorted_wid = sorted(wTypeAmount)
    for wTypeid in sorted_wid:
        date_ = sorted(wTypeAmount[wTypeid])
        date_and_salesamount = wTypeAmount[wTypeid]
        for date in date_:
            validateFile.write(wTypeid+","+date+","+str(date_and_salesamount[date])+"\n")
    validateFile.close()
#计算大类的月份销售
#返回的monthSales的结构为{大类id：{月份：销量}}
def wTypeMonthSales(wTypeFile,beginMonth,endMonth):
    csv_wType = csv.reader(open(wTypeFile,"r"))
    monthSales = {}
    for row in csv_wType:
        if(csv_wType.line_num==1):
            continue
        id = row[0]
        month = int(row[1][4:6])
        sales = int(row[2])
        if(len(id)!=2):
            exit("文件格式错误")
        if(month not in range(beginMonth,endMonth+1)):
            continue
        if(id not in monthSales):
            monthSales[id]={month:sales}
        elif(month not in monthSales[id]):
            monthSales[id][month] = sales
        else:
            monthSales[id][month] += sales
    return monthSales
#预测大类月销售
#输入的wTypeMonthSale的结构为{大类id：{月份：销量}}，a为指数平滑的参数
#返回的prediction的结构为{大类id:月份预测值}
def predictwTypeMonth(wTypeMonthSale,a):
    prediction = {}
    for id in wTypeMonthSale:
        months = sorted(wTypeMonthSale[id])
        future= 0
        for month in months:
            if(future==0):
                future = wTypeMonthSale[id][month]
            else:
                future = a*wTypeMonthSale[id][month]+(1-a)*future
        prediction[id] = round(future)
    return prediction
#计算中类占大类的比例
#返回的Ratio的结构为{大类id：{中类id：比例}}
def mTypeRatio(mTypeFile,beginMonth,endMonth):
    csv_reader = csv.reader(open(mTypeFile,"r"))
    ratio = {}
    for row in csv_reader:
        if(csv_reader.line_num==1):
            continue
        month = int(row[1][4:6])
        if(month not in range(beginMonth,endMonth)):
            continue
        wType = row[0][0:2]
        mType = row[0]
        salesAmount = int(row[2])
        if(wType not in ratio):
            ratio[wType]={mType:salesAmount}
        elif(mType not in ratio[wType]):
            ratio[wType][mType] = salesAmount
        else:
            ratio[wType][mType] += salesAmount
    for wType in ratio:
        total = 0
        for mType in ratio[wType]:
            total +=ratio[wType][mType]
        for mType in ratio[wType]:
            ratio[wType][mType] = float(ratio[wType][mType])/total
    return ratio
#预测中类的月份销售
#返回的prediction的结构为{中类id：月份预测值}
#将大类的月份预测值分别乘以其种类的比例，得到中类的预测值
def predictmTypeMonth(predictwType,ratio):
    prediction = {}
    for wTypeid in predictwType:
        prewType = predictwType[wTypeid]
        for mTypeid in ratio[wTypeid]:
            prediction[mTypeid] = round(ratio[wTypeid][mTypeid]*prewType)
    return prediction
#进行预测，生成预测文件
#输入大类的月份预测，中类的月份预测，预测月份的天数，输入文件名
def predictResult(predictionwType,predictionmType,days,inputFile):
    csv_reader = csv.reader(open(inputFile,"r"))
    output = open("predict result.csv","w")
    for row in csv_reader:
        if(csv_reader.line_num==1):
            output.write("编码,日期,销量\n")
            continue
        if(len(row[0])==4):
            if row[0] not in predictionmType:
                amount = 1
            else:
                amount = predictionmType[row[0]]/float(days)
            output.write(row[0]+","+row[1]+","+str(math.ceil(amount))+"\n")
        elif(len(row[0])==2):
            if row[0] not in predictionwType:
                amount = 15
            else:
                amount = predictionwType[row[0]]/float(days)
            output.write(row[0]+","+row[1]+","+str(math.ceil(amount))+"\n")
        else:
            exit("格式不正确")
#用四月份的数据验证
def validate(predictionwType,predictionmType,days,inputFile):
    csv_reader = csv.reader(open(inputFile, "r"))
    errorsqaresum = 0
    count = 0
    for row in csv_reader:
        if(csv_reader.line_num==1):
            continue
        if(len(row[0])==4):
            if(row[0] not in predictionmType):
                errorsqaresum += (int(row[2])-1)*(int(row[2])-1)
                count +=1
                continue
            predict = float(predictionmType[row[0]])/30
            errorsqaresum += (predict-int(row[2]))*(predict-int(row[2]))
            count +=1
        elif(len(row[0])==2):
            if(row[0] not in predictionwType):
                errorsqaresum +=(int(row[2])-15)*(int(row[2])-15)
                count +=1
                continue
            predict = float(predictionwType[row[0]])/30
            errorsqaresum += (predict-int(row[2]))*(predict-int(row[2]))
            count +=1
        else:
            exit("格式不正确")
    rmse = math.sqrt(float(errorsqaresum)/count)
    print("分数：%f" % (1/(1+rmse)))
wTypeMonthSale = wTypeMonthSales("wType_data.csv",1,3)
predictionwType = predictwTypeMonth(wTypeMonthSale,0.5)
ratio = mTypeRatio("mType_data.csv",1,3)
predictionmType = predictmTypeMonth(predictionwType,ratio)
validate(predictionwType,predictionmType,30,"validate_data")
#predictResult(predictionwType,predictionmType,30,"format_example.csv")


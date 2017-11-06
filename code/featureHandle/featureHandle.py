import pandas as pd
import numpy as np
import sys


"""a = pd.Series([1,3,3,4],index = [1,2,3,4])
b = pd.Series([8,5,4,5],index = [1,2,3,4])
c = pd.Series([3,1,9,6],index = [1,2,3,4])
x = pd.Series([9,495,6,7],index = [1,2,3,4])
d = pd.DataFrame({"a":a,"b":b,"c":c})
e = pd.DataFrame({'a':a,'c':c,'x':x})
for i in d.index:
    print(d.loc[i])"""
#print(pd.merge(d,e))
#print(d['c'].value_counts())
#获得大类特征向量
def category(zl):
    if(len(zl)!=4):
        exit("中类编码不正确")
    dl = zl[0:2]
    if(dl=="10"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="11"):
        return [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="12"):
        return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="13"):
        return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="14"):
        return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="15"):
        return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="20"):
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="21"):
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    elif(dl=="22"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    elif(dl=="23"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    elif(dl=="30"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    elif(dl=="31"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    elif(dl=="32"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    elif(dl=="33"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    elif(dl=="34"):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    else:
        exit("不存在的大类！")
#将日期字符串转换成距离2015年1月1日的天数
def dateTransformToNum(date):
    if(len(date)!=8):
        exit("数据格式错误！")
    month = int(date[4:6])
    date_ = int(date[6:8])
    if(month == 1):
        return date_
    elif(month == 2):
        return 31+date_
    elif(month==3):
        return 59+date_
    elif(month==4):
        return 90+date_
    elif(month == 5):
        return 120+date_
    else:
        exit("月份错误")
# 将距离2015年1月1日的天数转换成日期字符串
def dateTransferToString(date):
    if(date<=0):
        exit("日期不能为负值！")
    elif(date<=31):
        return "201501%02d" % date
    elif(date<=59):
        return "201502%02d" % (date-31)
    elif(date<=90):
        return "201503%02d" % (date-59)
    elif(date<=120):
        return "201504%02d" % (date-90)
    elif(date<=151):
        return "201505%02d" % (date-120)
    else:
        exit("日期超出范围！")
#输出中类在每一天的促销比率
def createOnSaleFile(originalFile):
    raw_data = pd.read_csv(originalFile)
    onSale = raw_data.groupby(["中类编码","小类编码","销售日期","是否促销",]).size()
    #开始计算种类的促销比率
    onSaleRate = {}
    onSaleCount = {}
    for index in onSale.index:
        if((index[0],index[2]) not in onSaleRate):
            onSaleRate[(index[0],index[2])]=1
        else:
            onSaleRate[(index[0],index[2])]+=1
        if(index[3]=='否'):
            continue
        if((index[0],index[2]) not in onSaleCount):
            onSaleCount[(index[0],index[2])]=1
        else:
            onSaleCount[(index[0],index[2])]+=1
    #计算大类的促销比率
    dlRate = {}
    dlCount = {}
    for key in onSaleRate:
        if((int(key[0]/100),key[1]) not in dlRate):
            dlRate[(int(key[0]/100),key[1])]= onSaleRate[key]
        else:
            dlRate[(int(key[0]/100), key[1])] += onSaleRate[key]

        if(key not in onSaleCount):
            onSaleRate[key]=0
        else:
            if((int(key[0]/100),key[1]) not in dlCount):
                dlCount[(int(key[0]/100),key[1])]=onSaleCount[key]
            else:
                dlCount[(int(key[0]/100), key[1])] += onSaleCount[key]
            onSaleRate[key]=onSaleCount[key]/onSaleRate[key]
    for key in dlRate:
        if(key not in dlCount):
            dlRate[key]=0
        else:
            dlRate[key]=dlCount[key]/dlRate[key]
    #将前四个月未出现的中类商品的促销比率设置为大类的促销比率
    """for i in range(1,121):
        date = dateTransferToString(i)
        index1 = (1507,int(date))
        index2 = (3208,int(date))
        index3 = (3311,int(date))
        index4 = (3413,int(date))
        if((15,int(date)) not in dlRate):
            onSaleRate[index1]=0
        else:
            onSaleRate[index1] = dlRate[(15,int(date))]
        if((32,int(date)) not in dlRate):
            onSaleRate[index2]=0
        else:
            onSaleRate[index2] = dlRate[(32,int(date))]
        if((33,int(date)) not in dlRate):
            onSaleRate[index3]=0
        else:
            onSaleRate[index3] = dlRate[(33,int(date))]
        if((34,int(date)) not in dlRate):
            onSaleRate[index4]=0
        else:
            onSaleRate[index4] = dlRate[(34,int(date))]"""

    output = open("on_sale_rate.csv","w")
    output.write("编码,日期,促销比率\n")
    sortOnSaleRate = sorted(onSaleRate)
    currentType = 0
    dateCount = 1
    for index in sortOnSaleRate:
        if(currentType==0):
            currentType=index[0]
            continue
        if(currentType!=index[0]):
            for i in range(dateCount,121):
                output.write(str(currentType)+","+
                             dateTransferToString(i)+","+"0\n")
            dateCount=1
            currentType=index[0]
        if(dateCount==dateTransformToNum(str(index[1]))):
            output.write(str(currentType)+","+dateTransferToString(dateCount)
                         +",%.3f\n" %onSaleRate[index])
            dateCount+=1
        else:
            for i in range(dateCount,121):
                if(i==dateTransformToNum(str(index[1]))):
                    output.write(str(currentType)+","+
                                 dateTransferToString(i)+",%.3f\n" %onSaleRate[index])
                    dateCount=i+1
                    break
                else:
                    output.write(str(currentType)+","+dateTransferToString(i)+",0\n")
    for i in range(dateCount, 121):
        output.write(str(currentType) + "," +
                     dateTransferToString(i) + "," + "0\n")
    output.close()
#是否工作日
def isWeekday(date):
    if(type(date)==int):
        return int((date+3)%7==6 or (date+3)%7==0)
    elif(type(date)==str):
        day =(dateTransformToNum(date)+3)%7
        return int(day==6 or day==0)
#是否休假
def isVocation(date):
    vocationDays = ["20150101","20150102","20150103","20150110",
                    "20150111","20150117","20150118","20150124",
                    "20150125","20150131","20150201","20150207",
                    "20150208","20150214","20150218","20150219",
                    "20150220","20150221","20150222","20150223",
                    "20150224","20150301","20150307","20150308",
                    "20150314","20150315","20150321","20150322",
                    "20150328","20150329","20150404","20150405",
                    "20150406","20150411","20150412","20150418",
                    "20150419","20150425","20150426"]
    if(type(date)==int):
        date = dateTransferToString(date)
    if(date in vocationDays):
        return int(True)
    return int(False)
#生成促销比率文件
#createOnSaleFile('raw_data.csv')
#将促销比率文件和销量合在一起
"""label = pd.read_csv("zlsalesAmount.csv")
onSaleRate = pd.read_csv("on_sale_rate.csv")
container = pd.merge(label,onSaleRate)
featureWithOnSaleRate = open("feature_with_on_sale_rate.csv","w")
featureWithOnSaleRate.write("编码,日期,促销比率,销量\n")
for index,row in container.iterrows():
    featureWithOnSaleRate.write("%d,%d,%.3f,%d\n" %(int(row["编码"]),
                                int(row["日期"]),row["促销比率"],int(row["销量"])))
"""
"""categoryLabel = ["肉禽","水产","蔬果","熟食","烘焙","日配",
                     "粮油","冲调","休闲","酒饮","洗化","家居","家电","文体","针织"]
    dlfeature = pd.Series(category(str(int(row["编码"]))),index=categoryLabel)
    temp1 = row.append(dlfeature)"""




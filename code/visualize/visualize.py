import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv,os,sys
import datetime
import matplotlib.dates as mdates
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
#按格式预处理销售数量
def preprocessSales(filename,outputFile):
    csv_reader = csv.reader(open(filename))
    output = open(outputFile,"w")
    currentid = ""
    dateCount = 1
    for row in csv_reader:
        if(csv_reader.line_num==1):
            output.write("编码,日期,销量\n")
            continue
        typeid = str(int(float(row[0])))
        datestring = str(int(float(row[1])))
        sales = row[2]
        if(currentid!=typeid):
            currentid = typeid
            dateCount = 1
        if(dateCount!=dateTransformToNum(datestring)):
            output.write(typeid+","+dateTransferToString(dateCount)+
                         ",0\n")
            dateCount+=1
        output.write(typeid+","+datestring+","+sales+"\n")
        dateCount+=1
    output.close()
#画图
def plotFigure(filename):
    csv_reader = csv.reader(open(filename))
    salesamount = []
    date = []
    currentType = ""
    if (not os.path.exists(sys.path[0] + "\\figure")):
        os.makedirs(sys.path[0] + "\\figure")
    for row in csv_reader:
        if(csv_reader.line_num==1):
            continue
        if(currentType==row[0]):
            salesamount.append(int(row[2]))
            date.append(datetime.date(int(row[1][0:4]),int(row[1][4:6]),int(row[1][6:8])))
            continue
        if(currentType!=""):
            plt.figure(currentType)
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            plt.plot(date, salesamount, "-")
            fig = plt.gcf()
            fig.savefig("figure\\"+currentType+".png")
        salesamount = [int(row[2])]
        date = [datetime.date(int(row[1][0:4]),int(row[1][4:6]),int(row[1][6:8]))]
        currentType = row[0]
    plt.figure(currentType)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.plot(date, salesamount, "-")
    fig = plt.gcf()
    fig.savefig("figure\\" + currentType + ".png")




#preprocessSales("fullTrain.csv","salesamount.csv")
plotFigure("salesamount.csv")
import datetime
import pandas as pd
import numpy as np
import math,os
#权重函数，得到一周周期内相匹配与不匹配的权重
def weight(date1,date2,match_weight = 100,unmatch_weight = 1):
    if(not isinstance(date1,datetime.date)):
        date1=date1.to_pydatetime().date()
    if(not isinstance(date2,datetime.date)):
        date2=date2.to_pydatetime().date()
    delta = (date1-date2).days
    dis = int((delta-1)/7)+1
    if(date1.weekday()==date2.weekday()):
        return match_weight/dis
    else:
        return 0
#预测指定日期的数量
def predict(predict_date,training_series,match_weight=100,unmatch_weight=1):
    up_sum = 0
    bottom_sum = 0
    for dayIndex in training_series.index:
        up_sum+=training_series[dayIndex]*weight\
            (predict_date,dayIndex,match_weight,unmatch_weight)
        bottom_sum +=weight(predict_date,dayIndex,match_weight,unmatch_weight)
    if(bottom_sum==0):
        return 0
    return up_sum/bottom_sum
#用rmse衡量，在验证数据上计算得到最合适的匹配权重，和最小rmse，不匹配权重为1
def calculateParameter(training_series,validation_series):
    proper_weight = 100
    min_rmse = 99999
    for w in range(2,1001):
        square_sum = 0
        for fd in validation_series.index:
            p = predict(fd,training_series,match_weight=w)
            square_sum+=(validation_series[fd]-p)**2

        if(len(validation_series)!=0):
            rmse = math.sqrt(square_sum/len(validation_series))
        else:
            return 100,0
        if(rmse<min_rmse):
            proper_weight = w
            min_rmse = rmse
    return proper_weight,min_rmse
#获取训练数据和验证数据
def getTrainingAndValidationData(id):
    salesamount = pd.read_csv("dataEliminatedNoise.csv")
    salesamount["日期"] = salesamount["日期"].map\
        (lambda x: "%s-%s-%s" % (str(x)[0:4], str(x)[4:6], str(x)[6:8]))
    salesamount["日期"] = pd.to_datetime(salesamount["日期"])
    salesamount12 = salesamount[salesamount["编码"] == id]

    salesamount2 = salesamount12[salesamount12["日期"] >= "2015-03-01"]

    training_df = salesamount2[salesamount2["日期"] < "2015-04-01"]
    training_df1 = salesamount12[salesamount12["日期"] < "2015-02-01"]
    training_df = pd.concat([training_df1, training_df])
    training_data = training_df["销量"]
    training_data.index = training_df["日期"]
    validation_df = salesamount12[salesamount12["日期"] >= "2015-04-01"]
    validation_data = validation_df["销量"]
    validation_data.index = validation_df["日期"]
    return training_data,validation_data
#获取包含2月份的训练数据和验证数据
def getTrainingAndValidationData2(id):
    salesamount = pd.read_csv("dataEliminatedNoise2.csv")
    salesamount["日期"] = salesamount["日期"].map\
        (lambda x: "%s-%s-%s" % (str(x)[0:4], str(x)[4:6], str(x)[6:8]))
    salesamount["日期"] = pd.to_datetime(salesamount["日期"])
    salesamount12 = salesamount[salesamount["编码"] == id]

    training_df = salesamount12[salesamount12["日期"] < "2015-04-01"]

    training_data = training_df["销量"]
    training_data.index = training_df["日期"]
    validation_df = salesamount12[salesamount12["日期"] >= "2015-04-01"]
    validation_data = validation_df["销量"]
    validation_data.index = validation_df["日期"]
    return training_data,validation_data
#所有一起预测

if(not os.path.exists("total_self_define4")):
    os.mkdir("total_self_define4")
predicted = []
templet = pd.read_csv("format_example.csv")
del templet["销量"]
for id in templet["编码"].unique():
    if(id in predicted):
        continue
    selected_templet = templet[templet["编码"]==id]
    training_data,validation_data = getTrainingAndValidationData2(id)
    param,rmse = calculateParameter(training_data,validation_data)
    predict_result = []
    for day in pd.date_range("20150501",periods=30):
        predict_result.append(predict(day,pd.concat
        ([training_data,validation_data]),match_weight=param))
    selected_templet["销量"]=predict_result
    selected_templet.to_csv("total_self_define4\\%d.csv"%id,index = None)

total_result = pd.DataFrame()
for id in templet["编码"].unique():
    part_result = pd.read_csv("total_self_define4\\%d.csv"%id)
    total_result = pd.concat([total_result,part_result])
total_result["销量"] = total_result["销量"].map(round)
total_result.to_csv("total_self_define4\\total_result.csv",index = None)
#param,rmse = calculateParameter(training_data,validation_data)
#print(param,rmse)
#print(calculateParameter(training_data,validation_data))
#一个一个的预测
"""
predict_result = []
for day in pd.date_range("20150501",periods=30):
    predict_result.append(predict(day,pd.concat
    ([training_data,validation_data]),match_weight=param))
output = open("temp30.csv",'w')
for i in predict_result:
    output.write('%d\n'% round(i))
"""
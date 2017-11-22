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
    #dis = int((delta-1)/7)+1
    if(date1.weekday()==date2.weekday()):
        return match_weight/delta
    else:
        return unmatch_weight/delta
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
    min_sum =99999
    for w in range(0,500):
        square_sum = 0
        for fd in validation_series.index:
            p = predict(fd,training_series,match_weight=w)
            square_sum+=(validation_series[fd]-p)**2

        if(len(validation_series)==0):
            return 500,0
        if(square_sum<min_sum):
            proper_weight = w
            min_sum = square_sum
    return proper_weight,min_sum
#获取训练数据和验证数据
def getTrainingAndValidationData(id):
    salesamount = pd.read_csv("train_eliminated_noise.csv")
    salesamount = salesamount[salesamount["编码"]==id]
    salesamount["日期"] = salesamount["日期"].map\
        (lambda x:pd.to_datetime("%s-%s-%s"%(str(x)[0:4],str(x)[4:6],str(x)[6:])))

    training_data_df = salesamount[salesamount["日期"]<"20150801"]
    training_data_df = training_data_df[training_data_df["日期"]>="20150501"]
    training_data = training_data_df["销量"]
    training_data.index = training_data_df["日期"]

    validation_data_df = salesamount[salesamount["日期"]>="20150801"]
    validation_data = validation_data_df["销量"]
    validation_data.index = validation_data_df["日期"]
    return training_data,validation_data


if(not os.path.exists("temp_result2")):
    os.mkdir("temp_result2")
templet = pd.read_csv("example.csv")
del templet["销量"]
sum = 0
for id in templet["编码"].unique():
    selected_templet = templet[templet["编码"] == id]
    selected_templet["日期"] = selected_templet["日期"].map\
    (lambda x:pd.to_datetime("%s-%s-%s"%(str(x)[0:4],str(x)[4:6],str(x)[6:])))
    training_data, validation_data = getTrainingAndValidationData(id)
    param, square_sum = calculateParameter(training_data, validation_data)
    predict_result = []
    sum+=square_sum
    for date in selected_templet["日期"]:
        predict_result.append(predict(date,pd.concat
        ([training_data,validation_data]),match_weight=param))
    selected_templet["销量"] = predict_result
    selected_templet.to_csv("temp_result2\\%d.csv"%id,index = None)
print("rmse :%f"%math.sqrt(sum/len(templet["日期"])))
total_result = pd.DataFrame()
for id in templet["编码"].unique():
    part_result = pd.read_csv("temp_result2\\%d.csv"%id)
    total_result = pd.concat([total_result,part_result])
total_result["销量"] = total_result["销量"].map(round)
total_result["日期"] = total_result["日期"].map(lambda x:x.replace("-",""))
total_result.to_csv("temp_result2\\total_result_1.0.csv",index = None)

"""temp = pd.read_csv("temp_result\\total_result_1.0.csv")
temp["日期"] = temp["日期"].map(lambda x:x.replace("-",""))
temp.to_csv("temp_result\\total_result_1.1.csv",index=None)
"""

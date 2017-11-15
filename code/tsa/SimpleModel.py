import pandas as pd
import os
from statsmodels.tsa.arima_model import ARIMA
def proper_model(data,maxpq):
    init_p = 0
    init_q = 0
    init_model = None
    init_bic = 99999
    for p in range(maxpq):
        for q in range(maxpq):
            try:
                model = ARIMA(data,order = (p,1,q)).fit()
            except:
                continue
            bic = model.bic
            if bic<init_bic:
                init_model = model
                init_p = p
                init_q = q
    return init_model
def experienced_model(data,maxpq):

    for q in range(maxpq+1):
        try:
            model = ARIMA(data,order = (7,1,q)).fit()
            return model
        except:
            continue
def categorize(id,data,mpList,spList,ipList):
    totalSales = data["销量"].sum()
    data["销量"] = data["销量"].astype(float)
    if (0.0 in data["销量"].value_counts() and
                data["销量"].value_counts()[0.0] >= 91):
        spList.append(id)
    elif (totalSales <= 120):
        ipList.append(id)
    else:
        mpList.append(id)
salesamount = pd.read_csv("salesamount.csv")
salesamount["日期"] = salesamount["日期"]\
    .map(lambda x:str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:])
salesamount["销量"] = salesamount["销量"].astype(float)
templet = pd.read_csv("format_example.csv")
del templet["销量"]

salesamount = salesamount[salesamount["日期"]>="2015-03-01"]
final_result = pd.DataFrame()
mpList = []
spList = []
ipList = []

if(not os.path.exists("34simplePredict")):
    os.mkdir("34simplePredict")

for id in templet["编码"].unique():
    selected_salesamount = salesamount[salesamount["编码"]==id]
    selected_templet = templet[templet["编码"]==id]
    if (len(selected_salesamount) == 0):
        predict_result = [0] * 30
        selected_templet["销量"] = predict_result
        selected_templet["销量"] = selected_templet["销量"].map(round)
        selected_templet.to_csv("34simplePredict\\%d.csv"%id, index=None)
        continue

    amount = selected_salesamount["销量"]
    date = selected_salesamount["日期"].map(pd.to_datetime)
    amount.index = date

    model = proper_model(amount,int(len(amount)/10))
    if (model == None):
        predict_result = [1] * 30
        selected_templet["销量"] = predict_result
        selected_templet["销量"] = selected_templet["销量"].map(round)
        selected_templet.to_csv("34simplePredict\\%d.csv"%id, index=None)
        continue
    predict_result,stderr,conf_int = model.forecast(30)
    if(len(predict_result)!=len(selected_templet)):
        exit("预测数据长度与模板长度不同")
    selected_templet["销量"] = predict_result
    selected_templet["销量"] = selected_templet["销量"].map(round)
    selected_templet.to_csv("34simplePredict\\%d.csv"%id,index=None)
    #final_result = pd.concat([final_result,selected_templet])
#final_result["销量"] = final_result["销量"].map(round)
#final_result.to_csv("predict_result2.0.csv",index=None)




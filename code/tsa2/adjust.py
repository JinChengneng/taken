import pandas as pd
import tools
import numpy as np
import datetime
import math
from statsmodels.tsa.seasonal import seasonal_decompose

salesamount = pd.read_csv("dataEliminatedNoise.csv")
salesamount["日期"] = salesamount["日期"].map\
    (lambda x:"%s-%s-%s"%(str(x)[0:4],str(x)[4:6],str(x)[6:8]))
salesamount = salesamount[salesamount["日期"]>="2015-03-01"]
salesamount1 = salesamount[salesamount["编码"]==12]
salesamount1["日期"] = pd.to_datetime(salesamount1["日期"])
salesamount1["星期"] = salesamount1["日期"].map(lambda x:x.weekday()+1)
print(salesamount1)
"""
train_data = salesamount1[salesamount1["日期"]<"2015-04-01"]
train_series = train_data["销量"]
train_series.index = train_data["日期"].map(pd.to_datetime)
trend,residual,seasonal_df = tools.decompose(train_series)
date = trend.index[-1].to_pydatetime()+datetime.timedelta(1)
trend = np.log(trend+1)
model = tools.ARIMA_model(trend,len(trend)/10)
predict,stderr,conf_int =model.forecast(30)
predict_df = pd.DataFrame({"日期":pd.date_range(date,periods=30).to_pydatetime(),"销量":predict})
predict_df["星期"] = predict_df["日期"].map(lambda x:x.weekday()+1)
predict_df["销量"] = predict_df["销量"].map(lambda x:np.exp(x)-1)
predict_df = pd.merge(predict_df,seasonal_df,on=["星期"])
predict_df["销量"] = predict_df["销量"]+predict_df["周期性"]

predict_df.rename(columns = {"销量":"预测销量"},inplace = True)

del salesamount1["编码"]
salesamount1["日期"] = pd.to_datetime(salesamount1["日期"])
predict_df.drop(["星期","周期性"],axis = 1,inplace = True)
rmse_df = pd.merge(salesamount1,predict_df,on=["日期"])
#print(salesamount1)
#print(predict_df)
rmse_df = rmse_df.dropna()
rmse_df["error"] = (rmse_df["销量"]-rmse_df["预测销量"])**2
rmse = rmse_df["error"].mean()
print(rmse_df)
"""
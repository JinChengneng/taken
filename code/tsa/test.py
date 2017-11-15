import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
import datetime,os
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose
# 移动平均图
def draw_trend(timeSeries, size):
    f = plt.figure(facecolor='white')
    # 对size个数据进行移动平均
    rol_mean = timeSeries.rolling(window=size).mean()
    # 对size个数据进行加权移动平均
    rol_weighted_mean = pd.ewma(timeSeries, span=size)

    timeSeries.plot(color='blue', label='Original')
    rol_mean.plot(color='red', label='Rolling Mean')
    rol_weighted_mean.plot(color='black', label='Weighted Rolling Mean')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show()

def draw_ts(timeSeries):
    f = plt.figure(facecolor='white')
    timeSeries.plot(color='blue')
    plt.show()
def testStationarity(ts):
    dftest = adfuller(ts)
    # 对上述函数求得的值进行语义描述
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistics','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    return dfoutput
# 自相关和偏相关图，默认阶数为31阶
def draw_acf_pacf(ts, lags=31):
    f = plt.figure(facecolor='white')
    ax1 = f.add_subplot(211)
    plot_acf(ts, lags=lags, ax=ax1)
    ax2 = f.add_subplot(212)
    plot_pacf(ts, lags=lags, ax=ax2)
    plt.show()
# 差分操作
def diff_ts(ts, d):
    global shift_ts_list
    #  动态预测第二日的值时所需要的差分序列
    global last_data_shift_list
    shift_ts_list = []
    last_data_shift_list = []
    tmp_ts = ts
    for i in d:
        last_data_shift_list.append(tmp_ts[-i])
        print (last_data_shift_list)
        shift_ts = tmp_ts.shift(i)
        shift_ts_list.append(shift_ts)
        tmp_ts = tmp_ts - shift_ts
    tmp_ts.dropna(inplace=True)
    return tmp_ts
# 还原操作
def predict_diff_recover(predict_value, d):
    if isinstance(predict_value, float):
        tmp_data = predict_value
        for i in range(len(d)):
            tmp_data = tmp_data + last_data_shift_list[-i-1]
    elif isinstance(predict_value, np.ndarray):
        tmp_data = predict_value[0]
        for i in range(len(d)):
            tmp_data = tmp_data + last_data_shift_list[-i-1]
    else:
        tmp_data = predict_value
        for i in range(len(d)):
            try:
                tmp_data = tmp_data.add(shift_ts_list[-i-1])
            except:
                raise ValueError('What you input is not pd.Series type!')
        tmp_data.dropna(inplace=True)
    return tmp_data
#绘制销量图
def plotSalesamount(data,name):
    date = data.index.to_pydatetime()
    amount = data.values

    plt.figure(name)
    ax = plt.gca()
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.plot(date, amount, "-")
    plt.show()
    return plt.gcf()
"""
amount = pd.read_csv("dataEliminatedNoise.csv")
amount10 = amount[amount["编码"]==10]
date = amount10["日期"].map(lambda x:pd.to_datetime(str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:]))
series_amount10 = amount10["销量"]
series_amount10.index = date
train = series_amount10[:90]
decomposition = seasonal_decompose(train,model="multipicative")
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plotSalesamount(trend,"trend")
plotSalesamount(seasonal,"seasonal")
plotSalesamount(residual,"residual")"""
#print(series_amount10)
#diff1 = diff_ts(series_amount10,d=[7,1])
#print(diff1)
#diff1.dropna(inplace = True)
#print(testStationarity(diff1))
#draw_acf_pacf(diff1)

#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox
#print("白噪声检验结果：",acorr_ljungbox(diff1,lags=1))
"""
model = ARIMA(train,order=(6,1,0))
result_arma = model.fit(disp=-1,method="css")
predict = result_arma.forecast(30)
result = pd.Series(predict[0],index=pd.date_range("2015-04-01",periods=30))
#shift = series_amount10.shift(1)
#recover_result = predict.add(shift)"""
"""
recover_result = predict_diff_recover(predict,d=[7,1])
print("recover result is ",recover_result)"""
#series_amount10 = series_amount10[recover_result.index]
"""plt.figure(facecolor="white")
series_amount10.plot(color = "red",label="origin")
result.plot(color="blue",label="predict")
plt.legend(loc = "best")

plt.show()
"""
"""from statsmodels.tsa.arima_model import ARMA
pmax = int(len(diff1)/10)
qmax = int(len(diff1)/10)

bic_matrix = []
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):

        try:
            tmp.append(ARMA(diff1,(p,q)).fit().bic)
        except:
            tmp.append(None)

    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix)
p,q = bic_matrix.stack().idxmin()
print("p和q的值为:",p,q)"""
""""""
"""
templet = pd.read_csv("format_example.csv")
del templet["销量"]
total = pd.DataFrame()
for id in templet["编码"].unique():
    temp = pd.read_csv("34simplePredict\\%d.csv"%id)
    total = pd.concat([total,temp])
total.to_csv("34simpleModelResult.csv",index = None)"""

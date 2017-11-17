import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
#绘制序列类型的图
def plotSeriesWithDateIndex(data,name):
    date = data.index.to_pydatetime()
    amount = data.values
    ax = plt.gca()
    ax.set_title(name)
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.plot(date, amount, "-")
    plt.show()
    return plt.gcf()
#绘制dataframe类型的图
def plotDataframeWithStringDate(selected_salesamount,name):
    if(len(selected_salesamount)==0):
        print("no data to plot!")
        return None
    d = selected_salesamount["日期"].map\
        (lambda x:datetime.date(int(x[0:4]),int(x[5:7]),int(x[8:])))
    amount = selected_salesamount[name]
    ax = plt.gca()
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.plot(d, amount, "-")
    return plt.gcf()
#中心滑动平均
def centralMovingAverage(data,windowSize):
    l = len(data)
    if(l<(2*windowSize+1)):
        raise "窗口大于数据长度！"
    smoothing_data = pd.Series([np.nan]*l, index=data.index)
    for i in range(windowSize, l-windowSize):
        sum = data[i-windowSize]*0.5+data[i+windowSize]*0.5
        for w in range(i-windowSize+1,i+windowSize-1):
            sum +=data[w]
        smoothing_data[i]=sum/(2*windowSize+1)
    return smoothing_data
#去除趋势项
def removeTrend(data,windowSize):
    smooth_data = centralMovingAverage(data,windowSize)
    plotSeriesWithDateIndex(smooth_data,"smooth_data")
    result = data/smooth_data
    return result.dropna()
#去除季节项
def removeSeasonal(data,no_trend_data):
    date = no_trend_data.index.to_pydatetime()
    amount = no_trend_data.values
    df = pd.DataFrame({"日期":date,"数量":amount})
    df["星期"] = df["日期"].map(lambda x:x.weekday()+1)
    seasonal = df.groupby(["星期"],as_index=False)["数量"].mean()
    seasonal["数量"] = seasonal["数量"]*7/seasonal["数量"].sum()
    seasonal.rename(columns = {"数量":"因子"},inplace = True)

    date = data.index.to_pydatetime()
    amount = data.values
    df = pd.DataFrame({"日期": date, "数量": amount})
    df["星期"] = df["日期"].map(lambda x: x.weekday() + 1)

    temp= pd.merge(df,seasonal,on=["星期"])
    temp["数量"] = temp["数量"]/temp["因子"]
    date = temp["日期"]
    amount= temp["数量"]
    amount.index = date
    return amount.sort_index()
#分解
def decompose(data,model = "additive"):
    decomposition = seasonal_decompose(data,model)
    seasonal = decomposition.seasonal[0:7]
    date = seasonal.index.to_pydatetime()
    seasonaldf = pd.DataFrame({"日期":date,"周期性":seasonal})
    seasonaldf["星期"] = seasonaldf["日期"].map(lambda x:x.weekday()+1)
    del seasonaldf["日期"]
    return decomposition.trend.dropna(),decomposition.resid.dropna(),seasonaldf
#获取合适的ARIMA模型
def ARIMA_model(data,maxpq):
    init_model = None
    init_bic = 99999
    for p in range(int(maxpq)+1):
        for q in range(int(maxpq)+1):
            try:
                model = ARIMA(data,order = (p,1,q)).fit()
            except:
                continue
            bic = model.bic
            if bic<init_bic:
                init_model = model
    return init_model

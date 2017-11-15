import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
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

#s = pd.Series([1,2,3,4,5,6,7,2,3],index=pd.date_range("20150101",periods=9))
#s2 = pd.Series([1,2,3],index=pd.date_range("20150102",periods=3))
#centralMovingAverage(s,1)
df = pd.read_csv("dataEliminatedNoise.csv")
df = df[df["编码"]==1001]
amount = df["销量"].map(round)
amount.index = pd.date_range("20150101",periods=len(amount))
plotSeriesWithDateIndex(amount,"salesamount")
no_trend_data = removeTrend(amount,7)
plotSeriesWithDateIndex(no_trend_data,"no_trend_data")
no_seasonal_data = removeSeasonal(amount,no_trend_data)
plotSeriesWithDateIndex(no_seasonal_data,"no_seasonal_data")

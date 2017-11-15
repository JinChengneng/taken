import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates
import datetime
def readFile():
    salesamount = pd.read_csv("dataEliminatedNoise.csv")
    salesamount["日期"] = salesamount["日期"].map\
        (lambda x: str(x)[0:4] + "-" + str(x)[4:6] + "-" + str(x)[6:])
    salesamount["销量"] = salesamount["销量"].astype(float)
    templet = pd.read_csv("format_example.csv")
    del templet["销量"]
    return salesamount,templet

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

def plotSalesamount(selected_salesamount):
    if(len(selected_salesamount)==0):
        return None
    d = selected_salesamount["日期"].map\
        (lambda x:datetime.date(int(x[0:4]),int(x[5:7]),int(x[8:])))
    amount = selected_salesamount["销量"]

    ax = plt.gca()
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.plot(d, amount, "-")
    return plt.gcf()
def plotCategorizedFigure(salesamount,mpList,spList,ipList):
    if(not os.path.exists("mpList")):
        os.mkdir("mpList")
    if (not os.path.exists("spList")):
        os.mkdir("spList")
    if (not os.path.exists("ipList")):
        os.mkdir("ipList")
    for mpProduct in mpList:
        selected_salesamount = salesamount\
        [salesamount["编码"] == mpProduct]
        figure = plotSalesamount(selected_salesamount)
        if(figure!=None):
            figure.savefig("mpList\\"+str(mpProduct)+".png")
    for spProduct in spList:
        selected_salesamount = salesamount \
            [salesamount["编码"] == spProduct]
        figure = plotSalesamount(selected_salesamount)
        if (figure != None):
            figure.savefig("spList\\"+str(spProduct)+".png")

    for ipProduct in ipList:
        selected_salesamount = salesamount \
            [salesamount["编码"] == ipProduct]
        figure = plotSalesamount(selected_salesamount)
        if (figure != None):
            figure.savefig("ipList\\"+str(ipProduct)+".png")


salesamount,templet = readFile()
mpList = []
spList = []
ipList = []

for id in templet["编码"].unique():
    selected_salesamount = salesamount[salesamount["编码"]==id]
    categorize(id,selected_salesamount,mpList,spList,ipList)

#print(templet["编码"].value_counts())
print(mpList,spList,ipList)

plotCategorizedFigure(salesamount,mpList,spList,ipList)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

amount = pd.read_csv("salesamount.csv",encoding = "gbk")
amount10 = amount[amount["编码"]==10]
series_amount10 = amount10["销量"]
series_amount10 = np.log(series_amount10)
series_amount10.plot()
fig = plt.figure()
ax1 = fig.add_subplot(111)
diff1 = series_amount10.diff(1)
diff1.plot(ax = ax1)
plt.show()
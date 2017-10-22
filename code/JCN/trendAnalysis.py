from __future__ import print_function

import csv

import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

input_csvFile = open("./saleAmountOfLargeType.csv", "r")
input_reader = csv.reader(input_csvFile)

data = []
for item in input_reader:
    if input_reader.line_num == 1:
        continue
    if(item[0] == '20'):
        data.append(item[2])

print(len(data))

data = np.array(data, dtype=np.float)
data = pd.Series(data)

data.index = pd.Index(sm.tsa.datetools.dates_from_range('1','115'))

data.plot(figsize=(20,8))
plt.show()
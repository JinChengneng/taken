import pandas as pd
import tools 
from statsmodels.tsa.seasonal import seasonal_decompose
total=pd.read_csv('dataEliminatedNoise.csv')
a=total[total['编码']==2209]
d=pd.date_range('20150101',periods=120)
b=a['销量']
c=pd.Series(b.values,d)
decompositions=seasonal_decompose(c,model='additive')
print(decompositions.seasonal)
tools.plotSeriesWithDateIndex(decompositions.trend,"trend")
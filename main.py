import numpy as np
import pandas as pd
#import yfinance as yf

#start application
filename='data/SPY.csv'
names=['date','open','high','low,Adjclose','volume']
df=pd.read_csv(filename,names=names)
df = pd.read_csv(filename, names=names)
names = ['date', 'open', 'high', 'low,Adjclose', 'volume']
#print column names
column_headers = list(df.columns.values)
print("The Column Header :", column_headers)
#end code comment
column='volume'
volmin=(df[column].min())

print("volmin:"+volmin)
#print("npavg:"+np.average([column]))
#volavg=np.mean(df['volume'])

print('helo colab')

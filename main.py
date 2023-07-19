from math import log10, floor
import numpy as np
import pandas as pd

#import yfinance as yf

#start application
filename='data/SPY.csv'
names=['date','open','high','low,Adjclose','volume']
df=pd.read_csv(filename,names=names).tail(-2).dropna(inplace=False)
df = pd.read_csv(filename, names=names)
names = ['date', 'open', 'high', 'low,Adjclose', 'volume']
#print column names
column_headers = list(df.columns.values)
print("The Column Header :", column_headers)
column='volume'
volmin=(df[column].min())
volmax=(df[column].dropna()
//print(volmin)
print("volmax:"+ volmax)

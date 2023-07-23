from math import log10, floor
import numpy as np
import pandas as pd

#import yfinance as yf

#start application
filename='data/SPY.csv'
names=['date','open','high','low,Adjclose','volume']
df=pd.read_csv(filename,names=names).tail(-1).dropna(inplace=True)
df = pd.read_csv(filename, names=names).tail(-1)
names = ['date', 'open', 'high', 'low,Adjclose', 'volume']
#print column names
column_headers = list(df.columns.values)
print("The Column Header :", column_headers)
column='volume'
volmin=(df[column].min())
volmax=(df[column].max())
volmedian=str((round(df[column].median())))
print("volmin:"+volmin)
print("volmax:"+ volmax)
print("volmedian:"+ volmedian)
# get range and volume percentile from previous day and find coorelation with proce movement the next day

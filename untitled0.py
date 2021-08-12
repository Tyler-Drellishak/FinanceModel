# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:25:11 2021

@author: Tyler
"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

#Getting the Data from Yahoo, saving it in the "Data" DataFrame indexed by Ticker

Ticker = 'CLF'
Start = '2018-01-01'
End = dt.datetime.today()

Data = pd.DataFrame(data = None)
Data[Ticker] = web.DataReader(Ticker, 'yahoo', start=Start)['Adj Close']
StartPrice = Data[Ticker][1]


#Calculating the daily return in percent change and counting the number of occurances
#within 1% intervals, this is stored as a list "Ys", converting this list to a 
#DataFrame called "Returns"

DataDifferences = Data.diff()

out = pd.DataFrame(index = Data.index[1:], columns = ['Daily change'])

for day in list(range(1,len(Data))):
    PercentChange = DataDifferences[Ticker][day] / Data[Ticker][day]
    out.iloc[day-1] = PercentChange

Ys = list()

for point in list(np.linspace(-1,1,201)):
    Ys.append(len(out[(out['Daily change'] > point-.005) & (out['Daily change'] < point+.005)])
)

Returns = pd.DataFrame(data = Ys, columns = ["Daily Percent Return Occurances"])
#sns.barplot(np.linspace(-1,1,201), Ys )

#weighting daily return probability based on the number of occurances in the list
TotalDays = int(Returns.sum())

PercentOccurance = pd.DataFrame()
PercentOccurance = Returns["Daily Percent Return Occurances"].div(TotalDays)

#Running the simulation by first rolling a random integer then comparing it to
SimsNum = int(10) 
DaysNum = TotalDays
IsList = list()
SimDF = pd.DataFrame(index = range(0,DaysNum), columns = range(0,SimsNum))

for Sim in range(0,SimsNum):
    StockPrice = StartPrice

    for days in range(0,DaysNum):
        roll = np.random.randint(1,TotalDays+1)
        SumCounter = 0
        i = 0
        
        while i < len(Returns):
            if (Returns["Daily Percent Return Occurances"][i] + SumCounter) < roll:
                SumCounter = Returns["Daily Percent Return Occurances"][i] + SumCounter
                i += 1
            else:
                #print(i)
                StockPrice = (((i+.05)/100)*StockPrice)
                print(StockPrice)
                SimDF[Sim][days] = StockPrice
                break
        pass
    pass

plt.plot(SimDF[range(0,SimsNum)])
plt.plot(SimDF.sum(axis = 1)/SimsNum)
Aver = out.mean()
print(Aver)

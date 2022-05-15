import time
from turtle import color, pos
import MetaTrader5 as mt5
import Indicateurs as ind
import matplotlib.pyplot as plt 
import yfinance as yf
import talib as tab
import numpy as np

df = ind.ydataframe(stock = "ETH-USD", start = '2021-10-10', interval='1h')

df['MACD'],df['Signal'],df['Hist'] = tab.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['SAR'] = tab.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2)
ind.ema(df,length=200,column='Close')
pos_ouv = False
pos_ouv_short = False
achat_bull = []
vente_bull = []
achat_bear = []
vente_bear = []
sl_bear = 0
tp_bear = 0
sl_bull = 0 
tp_bull = 0 
achat_bear_plot =[np.nan,np.nan]
vente_bear_plot = [np.nan,np.nan]
for i in range(2,len(df)) :
    if df['Close'][i] < df['200EMA_Close'][i] and pos_ouv_short == False :
        if df['Hist'][i] < 0 and df['SAR'][i] > df['Close'][i] and df['SAR'][i-1] < df['Close'][i-1] :
            achat_bear.append(df['Close'][i])
            sl_bear = (df['SAR'][i] + df['Close'][i])/2
            tp_bear = df['Close'][i] + (df['Close'][i] - df['SAR'][i]) 
            achat_bear_plot.append(df['Close'][i])
            vente_bear_plot.append(np.nan)     
            pos_ouv_short = True
        else : 
            achat_bear_plot.append(np.nan)     
            vente_bear_plot.append(np.nan)
    elif pos_ouv_short == True and df['Close'][i] < tp_bear : 
        vente_bear.append(df['Close'][i])
        vente_bear_plot.append(df['Close'][i])
        achat_bear_plot.append(np.nan)
        pos_ouv_short = False
    elif pos_ouv_short == True and df['Close'][i] > sl_bear : 
        vente_bear.append(df['Close'][i])
        vente_bear_plot.append(df['Close'][i])
        achat_bear_plot.append(np.nan)
        pos_ouv_short = False   
    else : 
        achat_bear_plot.append(np.nan)     
        vente_bear_plot.append(np.nan)

def pv_short(list1,list2) :
    res = []
    if len(list1)>len(list2) :
        for i in range(0,len(list2)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))
    if len(list1)<len(list2) :
        for i in range(0,len(list1)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))           
    if len(list1) == len(list2) :
        for i in range(0,len(list1)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))
    return res

def resultat(n,res) :
    x = n
    for i in range(1,len(res)):
        x= x + x*res[i]
    return x

plt.scatter(df.index, achat_bear_plot,color='green')
plt.scatter(df.index, vente_bear_plot,color='red')
plt.scatter(df.index,df['SAR'],color = 'grey')

res = pv_short(achat_bear,vente_bear)
print(res)
print(resultat(10000,res))

plt.plot(df.index,df['Close'])
plt.plot(df.index,df['200EMA_Close'],color = 'orange')
plt.show()








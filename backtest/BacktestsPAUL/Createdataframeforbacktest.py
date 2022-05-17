from cProfile import label
from pickle import TRUE
from turtle import back
from attr import NOTHING
from pandas import *
import pandas as pd
import yfinance as yf
import requests as rq
from binance import *
import asyncio
import json
import requests
import time
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import *
from math import *
from decimal import *
import Indicateursbacktest as ind
#get unix TIME
#On va faire ça avec l'api binance
api_key = '0W0NnouXJG5kHRuvjm7AcZNOSYxHHPmNWItts8ZUWcIp9aQv4QyCKUa1EbRTE4Iw'
api_secret = 'NmW0ruph3E8qvg5c9c9ngEgukPVkHKCHYBPE27ZB8UBtD7kvI79JiWQDU7SXbwrF'
client = Client(api_key, api_secret)

# info = client.get_account_snapshot(type='SPOT')
# for infos in info['snapshotVos'][0]['data']['balances']:
#     print(infos)
def dataframe(filename, timeframe : str, Starttime : int ,backtest : bool, pair : str):
    #fonction qui renvoit la data depuis le temps spécifié
    #pour prendre les datas et faire moins de calcul (ou pas) ca doit etre possible d'actualiser que les datas qui sont nouvelles
    if timeframe == '5m':
        timeframe =  client.KLINE_INTERVAL_5MINUTE
    elif timeframe == '1m':
        timeframe = client.KLINE_INTERVAL_1MINUTE
    elif timeframe == '15m':
        timeframe = client.KLINE_INTERVAL_15MINUTE
    elif timeframe == '1h':
        timeframe = client.KLINE_INTERVAL_1HOUR
    elif timeframe == '2h':
        timeframe = client.KLINE_INTERVAL_2HOUR
    elif timeframe == '4h':
        timeframe = client.KLINE_INTERVAL_4HOUR
    elif timeframe == '1d':
        timeframe = client.KLINE_INTERVAL_1DAY
    klines = client.get_historical_klines(pair, timeframe, Starttime)
    Lopen = []
    Lhigh = []
    Llow = []
    Lclose = []
    Ldates = []
    for k in klines:
        Lopen.append(float(k[1])) #Open
        Lhigh.append(float(k[2])) #High
        Llow.append(float(k[3])) #Low
        Lclose.append(float(k[4])) #Close
        Ldates.append(int(k[0]/1000))

    d = {'date': Ldates, 'open' : Lopen, 'high' : Lhigh, 'low' : Llow, 'price' : Lclose}
    # with open('recentdata.json','w+') as doc:
    #     json.dump(d, doc)
    df = pd.DataFrame(d)
    dataframe = df.reset_index(drop = True)
    ind.PSAR(dataframe)
    ind.zscore(dataframe, 20, "price")
    ind.sma(dataframe,20, '20Zscore_price')
    ind.sma(dataframe, 7, 'price')
    ind.MACD(dataframe, 'price')
    # dataframe = dataframe.drop(labels = 'index',axis = 1)

    if backtest:
        dataframe.to_pickle(filename)  
    return dataframe




# dataframe6mois1mBTC = dataframe('dataframe6mois1mBTC', '1m', 1629756000000, True, 'BTCUSDT')
# dataframe6mois1mBTC.to_pickle('./dataframe6mois1mBTC') #last tf at 337587 rn

# dataframe6mois5mBTC = dataframe('dataframe6mois5mBTC', '5m', 1629756000000, True, 'BTCUSDT')
# dataframe6mois5mBTC.to_pickle('./dataframe6mois5mBTC') 
dataframe6mois5mBTC = pd.read_pickle("./dataframe6mois5mBTC") #last tf at 67514 rn

# dataframe6mois4hBTC = dataframe('dataframe6mois4hBTC', '4h', 1629756000000, True, 'BTCUSDT')
dataframe6mois4hBTC = pd.read_pickle('./dataframe6mois4hBTC')
# dataframe6mois4hBTC.to_pickle('./dataframe6mois4hBTC')
# dataframe6mois5m.plot(y = 'price', use_index = True)
# dataframe6mois1m.plot(y = 'price', use_index = True)



# outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
# otherindex = dataframe6mois5m.loc[dataframe6mois5m['date'] == entryTimestamp,'price'].index[0]
# currentPrice1m = dataframe6mois1m.loc[index+4,'price']
# currentPrice5m = dataframe6mois5m.loc[index,'price']

# print(entryTime)
# print(outTime)
# print(currentPrice1m)
# print(currentPrice5m)
# print(index)

# for k in range(0,11):

#     print(dataframe6mois1m.loc[dataframe6mois1m['date'] == 1629756000+k*60,'price']
# print(dataframe6mois1m.iloc[-200:-150])
# print(dataframe6mois5m.iloc[-4:])
# print(datetime.utcfromtimestamp(1639460000 ).strftime('%Y-%m-%d %H:%M:%S'))

print(dataframe6mois5mBTC.loc[:,'7SMA_price']) #iloc[-20:,3:9]

# L = np.linspace(0,200,200)
# Lzscore = []
# LzscoreMA = []
# L3 = []
# Lprice = []


# fig, (ax1, ax2) = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# plt.plot(L,Lzscore)
# plt.plot(L,LzscoreMA)
# plt.plot(L,L3)
# ax2.plot(L, Lprice)
# plt.show()
# fig, (ax1, ax2) = plt.subplots(2)

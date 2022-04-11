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
    ind.MACD(dataframe, "price")
    ind.zscore(dataframe, 20, "price")
    ind.sma(dataframe,20, '20Zscore_price')
    # dataframe = dataframe.drop(labels = 'index',axis = 1)

    if backtest:
        dataframe.to_pickle(filename)  
    return dataframe

def realstd(dataframe,length,backtest):
    #Il faut que la dataframe que l'on passe à l'intérieur soit une seule colonne. On nous renverra une seule colonne aussi.
    #Si on passe une dataframe avec plusieurs colonnes on nous renvoit un dataframe avec plusieurs colonnes à la fin
    #Et le std calculé sur toutes les colonnes.
    if backtest == 'True':
        std = dataframe.rolling(length,0).std()
        return std
    else:
        std = dataframe.rolling(length,0).std()
        std = std.iloc[-20]
        return std


def std(dataframe,length):
    return dataframe.rolling(length).std()['colonne1']

def MA(dataframe,length):
    return dataframe.rolling(length).mean()

def Zscore(dataframe,length, backtest,indice):
    #Return Currentzscore, zscoredataframe
    #Ici on est obligé de mettre qu'une seule colonne en entrée sinon on applique le calcul sur toutes les colonnes ce quui
    #Indice pas nécéssaire au niveau du live trading
    #N'est pas intéréssant
    if backtest == 'True':
        displacement = dataframe - MA(dataframe,length)
        displacement = displacement.reset_index(drop = True)
        zScore = displacement.divide(realstd(dataframe,length, backtest))
        currentZscore = zScore.iloc[indice]
        return currentZscore, zScore
    else:
        displacement = dataframe - MA(dataframe,length)
        displacement = displacement.iloc[-length:]
        displacement = displacement.reset_index(drop = True)
        zScore = displacement.divide(realstd(dataframe,length, backtest))
        currentZscore = zScore.iloc[-1]
        return currentZscore, zScore

def CurrentzscoreMA(dataframe,length, backtest, indice):
    if backtest == 'True':
        zScoreMA = Zscore(dataframe,length, backtest, indice)[1].rolling(length).mean()
        currentZscoreMA = zScoreMA.iloc[indice]
        return currentZscoreMA, zScoreMA
    else:
        zScoreMA = Zscore(dataframe,length, backtest, indice)[1].rolling(length).mean()
        currentZscoreMA = zScoreMA.iloc[-1]
        return currentZscoreMA, zScoreMA

# def zranklo = 

# file = open('dataframe6mois.json')



dataframe6mois5m = pd.read_pickle("./dataframe6mois5m.pkl")

# dataframe6mois4hBTC = dataframe('dataframe6mois4hBTC', '4h', 1629756000000, True, 'BTCUSDT')
dataframe6mois4hBTC = pd.read_pickle('./dataframe6mois4hBTC')

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
print(dataframe6mois4hBTC.loc[:,'PSAR'])

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
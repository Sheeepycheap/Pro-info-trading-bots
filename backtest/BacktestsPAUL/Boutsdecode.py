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
#get unix TIME
#On va faire ça avec l'api binance
api_key = '0W0NnouXJG5kHRuvjm7AcZNOSYxHHPmNWItts8ZUWcIp9aQv4QyCKUa1EbRTE4Iw'
api_secret = 'NmW0ruph3E8qvg5c9c9ngEgukPVkHKCHYBPE27ZB8UBtD7kvI79JiWQDU7SXbwrF'
client = Client(api_key, api_secret)

# info = client.get_account_snapshot(type='SPOT')
# for infos in info['snapshotVos'][0]['data']['balances']:
#     print(infos)
def dataframe(filename,timeframe, Starttime,backtest):
    #fonction qui renvoit la data depuis le temps spécifié
    #pour prendre les datas et faire moins de calcul (ou pas) ca doit etre possible d'actualiser que les datas qui sont nouvelles
    #Je vais faire ca dans une fonction (toutes les 5 min on appel l'autre pute une fois sur une data et on met à jour le doc des datas)
    #Les étapes c'est début du prog on initialise le doc après open supprimer derniere et ajouter premiere (very easy)
    if timeframe == '5m':
        timeframe =  client.KLINE_INTERVAL_5MINUTE
    elif timeframe == '1m':
        timeframe = client.KLINE_INTERVAL_1MINUTE
    klines = client.get_historical_klines("BTCUSDT", timeframe, Starttime)
    L = []
    Ldates = []
    for k in klines:
        L.append(float(k[4]))
        Ldates.append(int(k[0])/1000)

    d = {'date': Ldates, 'price' : L }
    # with open('recentdata.json','w+') as doc:
    #     json.dump(d, doc)
    df = pd.DataFrame(d)
    dataframe = df.reset_index(drop = True)
    useddataframe = dataframe.loc[:,'price']
    dataframezscoreMA = CurrentzscoreMA(useddataframe,20, 'True', 0)[1]\
            .reset_index(name="zscoreMA")
    zscore = Zscore(useddataframe,20, 'True',0)[1]\
            .reset_index(name="zscore")

    dataframe = pd.concat([dataframe,zscore, dataframezscoreMA], axis=1)
    dataframe = dataframe.drop(labels = 'index',axis = 1)
    if backtest == 'True':
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

# dataframe = dataframe('dataframe6mois1m.pkl','1m', 1629756000000,'True')



dataframe6mois1m = pd.read_pickle("./dataframe6mois1m.pkl")
dataframe6mois5m = pd.read_pickle("./dataframe6mois5m.pkl")

dataframe6mois5m.plot(y = 'price', use_index = True)


 

# entryTimestamp = dataframe6mois5m.loc[0,'date']

# dataframe = pd.read_pickle("./dataframe6mois5m.pkl")
# MA20 = MA(dataframe6mois5m.loc[:,'price'],20)\
#             .reset_index(name="MA20")
# dataframe = pd.concat([dataframe6mois5m,MA20], axis=1)
# dataframe = dataframe.drop(labels = 'index', axis = 1)
# dataframe.to_pickle("./dataframe6mois5m.pkl") 
# print(dataframe6mois5m.iloc[-20:])
# entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
# index = dataframe6mois5m.loc[dataframe6mois5m['date'] == 	1633057200,'price'].index[0]
def createrangefilter(data1, data2, indice) -> pd.DataFrame:
    #""
    #Range filter. 
    #Creation de la colonne rangefilter à partir du reste on parcourt toute la bdd de base
    #On ajoute les valeurs à chaque ligne comme si on fesait du live trading
    #""
    # print(str(indice) + ' ' + str(rngfilt))

    #On initialise le rangefilter
    rangefilter = pd.Dataframe({'rngfilter' : [0]})
    for k in range(len(data1.index)):
        if data1.loc[k,'price'] > rangefilter.iloc[-1,0] :
            if data1.loc[k,'price'] - data2.loc[k] < rangefilter.iloc[-1,0]:
                rangefilter.loc[rangefilter.shape[0]] = rangefilter.iloc[-1,0]
            else:
                rangefilter.loc[rangefilter.shape[0]] = data1.loc[k,'price'] - data2.loc[k]
        else : 
            if data1.loc[k,'price'] + data2.loc[k] > rangefilter.iloc[-1,0]:
                rangefilter.loc[rangefilter.shape[0]] = rangefilter.iloc[-1,0]
            else :
                rangefilter.loc[rangefilter.shape[0]] = data1.loc[k,'price'] + data2.loc[k]
    data1["Range_filter"] = rangefilter

plt.show()
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
# print(datetime.utcfromtimestamp((len(dataframe6mois)-30000)*300 +1629756000 ).strftime('%Y-%m-%d %H:%M:%S'))
# L = np.linspace(0,200,200)
# Lzscore = []
# LzscoreMA = []
# L3 = []
# Lprice = []
# for k in range(0,200):
#     Lzscore.append(dataframe6mois.loc[len(dataframe6mois)-k-1,'zscore'])
#     LzscoreMA.append(dataframe6mois.loc[len(dataframe6mois)-k-1,'zscoreMA'])
#     Lprice.append(dataframe6mois.loc[len(dataframe6mois)-k-1,'price'])
#     L3.append(3)
# Lzscore.reverse()
# LzscoreMA.reverse()
# Lprice.reverse()

# fig, (ax1, ax2) = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# plt.plot(L,Lzscore)
# plt.plot(L,LzscoreMA)
# plt.plot(L,L3)
# ax2.plot(L, Lprice)
# plt.show()
# fig, (ax1, ax2) = plt.subplots(2)


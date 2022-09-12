from cProfile import label
from pickle import TRUE
from turtle import back
from attr import NOTHING
from pandas import *
import pandas as pd
import yfinance as yf
import requests as rq
from binance import *
import time as time
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
import datetime as datetime
from math import *
from decimal import *
import Indicateursbacktest as ind

#On va faire ça avec l'api binance
#Clefs qui doivent etre passées en privées 

#Pour récupérer des informations a propose de symboles on a besoin des clefs apis binance 
#Ces dernieres sont à insérer ci dessous 
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)


def dataframe(filename, timeframe : str, Starttime : int ,backtest : bool, pair : str):
    """
    Fonction qui renvoit la data depuis le temps spécifié.
    Créé une dataframe à partir de différentes données spécifiées

    ---
    Paramètres
    ---

    -La timeframe (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d)

    -Le temps de début en unix à 10 digit (donc milli secondes)

    -Backtest : True si les données doivent etre sauvegardés pour pouvoir travailler dessus ou False si c'est des données à utiliser en live trading
    
    -La paire avec "pair" : Toutes les paires disponibles sur binance sont récupérables. Par exemple : BTCUSDT renvoie les différents prix du bitcoin en fonction du prix du dollar.

    ---
    Remarques
    ---
    On n'effectue pas de calculs des indicateurs sur la dataframe 1 minutes car, on n'élabore pas de stratégies sur une timeframe aussi faible (trop volatile) et le temps de calcul des indacateurs est
    très long
    """
    #Ici choix de la timeframe
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
    
    #création des bougies passées:
    klines = client.get_historical_klines(pair, timeframe, Starttime)
    Lopen = []
    Lhigh = []
    Llow = []
    Lclose = []
    Ldates = []
    #création des liste pour la base de données
    for k in klines:
        Lopen.append(float(k[1])) #Open
        Lhigh.append(float(k[2])) #High
        Llow.append(float(k[3])) #Low
        Lclose.append(float(k[4])) #Close
        Ldates.append(int(k[0]/1000))

    d = {'date': Ldates, 'open' : Lopen, 'high' : Lhigh, 'low' : Llow, 'price' : Lclose}
    
    df = pd.DataFrame(d)
    dataframe = df.reset_index(drop = True)
    if timeframe != '1m':
        ind.PSAR(dataframe)
        ind.zscore(dataframe, 20, "price")
        ind.sma(dataframe,20, '20Zscore_price')
        ind.sma(dataframe, 7, 'price')
        ind.MACD(dataframe, 'price')
    

    if backtest:
        dataframe.to_pickle(filename)  
    return dataframe


"""
Ci dessus est le code juste pour permettre à l'utilisateur de rentrer les données pour créer la dataframe qui est intéréssante à backtester
Il suffit de répondre aux questions possées lors du lancement du code 
Il y a une gestion des erreurs dans le cas ou les données proposées ne correspondent pas aux données attendus
"""
backtest = input("Voulez vous download une dataframe? (True or False) ")
if backtest == 'True':
    timeframe = input("Choisissez une timeframe : (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d) ")
    timestart = input("Choisissez un temps unix en milliseconde pour démarer la création de dataframe : ")
    try:
        timestart = int(timestart)
        test1 = timestart/(10**12)
        if int(test1) !=1:
            timestart = 1629756000000 #valeur par défault
            print('timestart value is not usuable default value 1629756000000 has been used')
        test2 = timestart - ceil(timestart/10)*10
        if int(test2) != 0:
            timestart = 1629756000000 #valeur par défault
            print('timestart value is not usuable default value 1629756000000 has been used')
    except:
        timestart = 1629756000000
        print('timestart value is not usuable default value 1629756000000 has been used')
    paire = input('Choisissez la paire pour la base de données (Ex: BTCUSDT) : ')
    lengthofdataframe = round((int(time.time()) - timestart/1000)/(3600*24*30),1)
    name = "dataframe" + str(lengthofdataframe) + 'mois' + timeframe + paire
    dataframe1 = dataframe(name, timeframe, timestart, True, paire)






""""
# TESTS NON UTILES
"""

# dataframe6mois5mBTC = dataframe('dataframe6mois5mBTC', '5m', 1629756000000, True, 'BTCUSDT')
# dataframe6mois5mBTC.to_pickle('./dataframe6mois5mBTC') 
# dataframe6mois5mBTC = pd.read_pickle("dataframe9.3mois1mBTCUSDT") #last tf at 67514 rn
# print(dataframe6mois5mBTC.loc[26700:,'price':'PSARdir'])
# print(dataframe6mois5mBTC.iloc[-4:,:])
# dataframe6mois4hBTC = dataframe('dataframe6mois4hBTC', '4h', 1629756000000, True, 'BTCUSDT')
# dataframe6mois4hBTC = pd.read_pickle('./dataframe6mois4hBTC')
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

# print(datetime.utcfromtimestamp(1639460000 ).strftime('%Y-%m-%d %H:%M:%S'))

# print(dataframe6mois5mBTC.loc[:,'7SMA_price']) #iloc[-20:,3:9] 

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

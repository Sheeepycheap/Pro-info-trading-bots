from pickle import TRUE
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
from datetime import datetime
from math import *
from decimal import *


#get unix TIME
#On va faire ça avec l'api binance
api_key = '0W0NnouXJG5kHRuvjm7AcZNOSYxHHPmNWItts8ZUWcIp9aQv4QyCKUa1EbRTE4Iw'
api_secret = 'NmW0ruph3E8qvg5c9c9ngEgukPVkHKCHYBPE27ZB8UBtD7kvI79JiWQDU7SXbwrF'
client = Client(api_key, api_secret)





# dataframe pour 6 mois en 5 miutes pour backtester



# Dans les lignes suivantes on ouvre un fichier et on écrit du json dedans mais pas besoin
# with open('btc_bars.json', 'w') as e:
#     json.dump(klines, e)
# Pour plot : 
def plot(x,y1,y2):
    plt.plot(x, y1, color='r', label='20Zscore_price')
    plt.plot(x, y2, color='g', label='20SMA_20Zscore_price')
    plt.show()

# zscoreused =  []
# zcoreemaused = []
# Data btc pour backtester

#select time data de 0 à 52985 avec 52985 = 24/02/2022 
def Selecttime(dataframe,startime, endtime):
    Lx = []
    for k in range(startime,endtime+1):
        
        Lx.append(dataframe.loc[k,'date'])
    return Lx


dataframe6mois5m = pd.read_pickle("./dataframe6mois5mBTC")
dataframe6mois1m = pd.read_pickle("./dataframe6mois1mBTC")

LCapital = [1000]
Lprice = []
Lindex = []
async def main(filename,backtest,start,end):
    TP = 0.003
    SL = 0.001
    file = open(filename, 'w+')
    entryTime = start
    typetrade = 'long'
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCours = False
    Capital = 1000
    if backtest == 'True':
        #On veut monitor le trade en cours donc dans le while, on va regarder le prix toutes les minutes



#
#Truc habituel en dessous:
#
        Entryprice = 0
        LzScore = [dataframe6mois5m.loc[start,'20Zscore_price']]
        LzScoreMA = [dataframe6mois5m.loc[start,'20SMA_20Zscore_price']]
        Gainmoyentrade = 0 
        Winrate = 0 
        #Strategie va etre : sell when 20Zscore_price < currentMA
        #Close trade when 20Zscore_price = currentMA
        #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
        k = Decimal(start)
        Bornes = 0
        while k < end:
            k+=Decimal(1)
            LzScore.append(dataframe6mois5m.loc[int(k),'20Zscore_price'])
            LzScoreMA.append(dataframe6mois5m.loc[int(k),'20SMA_20Zscore_price'])
            LCapital.append(Capital)
            if dataframe6mois5m.loc[int(k)-1,'20Zscore_price'] >= 2.4 and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1, '20Zscore_price']:
                Bornes = 1
            if  dataframe6mois5m.loc[int(k)-1,'20Zscore_price'] <= -2.4 and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1, '20Zscore_price']:
                Bornes = -1
                
            #Short condition
            if Bornes == 1 :
                typetrade = 'short' 
                # print('entrée dans trade')
                Bornes = 0 
                Entryprice = dataframe6mois5m.loc[int(k),'price']
                entryTimestamp = dataframe6mois5m.loc[int(k),'date']
                entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                #on initialise les datas pour la timeframe 1m
                index = dataframe6mois1m.loc[dataframe6mois1m['date'] == entryTimestamp+240,'price'].index[0]
                Lindex.append(dataframe6mois1m.loc[index,'date'])
                Lprice.append(dataframe6mois5m.loc[int(k),'price'])
                enCours = True
                # while enCours:
                while dataframe6mois5m.loc[int(k)-1,'20Zscore_price'] > -2.4 and k<end or enCours and k< end: #currentZscore1m >= 0
                    #ici on passe sur la dataframe une minute
                    #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                    
                    index +=1
                    k = Decimal(str(k)) + Decimal('0.2')
                    Lindex.append(dataframe6mois1m.loc[index,'date'])
                    Lprice.append(dataframe6mois1m.loc[index,'price'])
                    if Decimal(str(k))%1 == 0.0:
                        # LzScore.append(dataframe6mois5m.loc[int(k),'20Zscore_price'])
                        # LzScoreMA.append(dataframe6mois5m.loc[int(k),'20SMA_20Zscore_price'])
                        LCapital.append(Capital)
                    if (Entryprice-dataframe6mois1m.loc[index,'price'])/Entryprice > 0.0165:
                        enCours = False
                        break
                    if (dataframe6mois1m.loc[index,'price']-Entryprice)/Entryprice > 0.0012:
                        enCours = False
                        break

                outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
                Outprice = dataframe6mois1m.loc[index,'price']
                #Donc faut arreter le backtesting si le capital tombe à 0 
                Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
                if Resultattrade >= 0:
                    Winrate +=1
                Capital = Capital + Resultattrade
                nombreDeTrade+=1
                Gainmoyentrade += Resultattrade
                ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
                with open(filename, 'a+') as e:
                    json.dump(ClosedTrade, e)
                if not Decimal(str(k))%1 == 0.0:
                    k = Decimal(ceil(k))
                    # LzScore.append(dataframe6mois5m.loc[int(k),'20Zscore_price'])
                    # LzScoreMA.append(dataframe6mois5m.loc[int(k),'20SMA_20Zscore_price'])
                    LCapital.append(Capital)

# ""
# Long condition
# ""
            # if Bornes == -1 :
            #     typetrade = 'long'
            #     # print('entrée dans trade')
            #     Bornes = 0 
            #     Entryprice = dataframe6mois5m.loc[int(k),'price']
            #     entryTimestamp = dataframe6mois5m.loc[int(k),'date']
            #     entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            #     #on initialise les datas pour la timeframe 1m
            #     index = dataframe6mois1m.loc[dataframe6mois1m['date'] == entryTimestamp+240,'price'].index[0]
            #     Lindex.append(dataframe6mois1m.loc[index,'date'])
            #     Lprice.append(dataframe6mois5m.loc[int(k),'price'])
            #     enCours = True
            #     # while enCours:
            #     while dataframe6mois5m.loc[int(k)-1,'20Zscore_price'] < 2.4 and k<end or enCours: #currentZscore1m >= 0
            #         #ici on passe sur la dataframe une minute
            #         #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                    
            #         index +=1
            #         k = Decimal(str(k)) + Decimal('0.2')
            #         Lindex.append(dataframe6mois1m.loc[index,'date'])
            #         Lprice.append(dataframe6mois1m.loc[index,'price'])
            #         # print(dataframe6mois1m.loc[index, ['price','date']])
            #         if Decimal(str(k))%1 == 0.0:
            #             LzScore.append(dataframe6mois5m.loc[int(k),'20Zscore_price'])
            #             LzScoreMA.append(dataframe6mois5m.loc[int(k),'20SMA_20Zscore_price'])
            #             LCapital.append(Capital)
            #         if (dataframe6mois1m.loc[index,'price']- Entryprice)/Entryprice > 0.005:
            #             enCours = False
            #             break
            #         if (Entryprice - dataframe6mois1m.loc[index,'price'])/Entryprice > 0.003:
            #             enCours = False
            #             break

            #     outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
            #     Outprice = dataframe6mois1m.loc[index,'price']
            #     #Donc faut arreter le backtesting si le capital tombe à 0 
            #     Resultattrade = Capital * (Outprice-Entryprice)/Entryprice
            #     Capital = Capital + Resultattrade
            #     nombreDeTrade+=1
            #     ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            #     with open(filename, 'a+') as e:
            #         json.dump(ClosedTrade, e)
            #     if not Decimal(str(k))%1 == 0.0:
            #         k = Decimal(ceil(k))
            #         LzScore.append(dataframe6mois5m.loc[int(k),'20Zscore_price'])
            #         LzScoreMA.append(dataframe6mois5m.loc[int(k),'20SMA_20Zscore_price'])
            #         LCapital.append(Capital)
    # else:    

    #     #a update dans la boucle
    #     now = int( time.time() )*1000
    #     From = now - 14400000
    #     df = dataframe('5m', From)
    #     zScore = Zscore(df,20)[0]
    #     currentZscoreMA = CurrentzscoreMA(df,20)[0]
    #     currentPrice = df.iloc[-1].loc['colonne1']
    #     Entryprice = 0
    #     #Strategie va etre : sell when 20Zscore_price < currentMA
    #     #Close trade when 20Zscore_price = currentMA
    #     #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
    #     while TRUE:
    #         print(zScore, currentZscoreMA)
    #         if zScore < currentZscoreMA:
    #             Entryprice = currentPrice
    #             while zScore < currentZscoreMA:
    #                 await asyncio.sleep(300)
    #                 #On update dans la boucle toutes les 5 min pour avoir les dernieres données 
    #                 now = int( time.time() )*1000
    #                 From = now - 14400000
    #                 df = dataframe('5m', From)
    #                 zScore = Zscore(df,20)[0]
    #                 currentZscoreMA = CurrentzscoreMA(df,20)[0]
    #                 currentPrice = df.iloc[-1].loc['colonne1']
    #                 print(zScore, currentZscoreMA)
    #             Outprice = currentPrice
    #             Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
    #             Capital = Capital + Resultattrade
    #             ClosedTrade = {'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital }
    #             print("trade done !")
    #             with open(filename, 'a+') as e:
    #                 json.dump(ClosedTrade, e)
    #         else:
                
    #             await asyncio.sleep(300)
    #             now = int( time.time() )*1000
    #             From = now - 14400000
    #             df = dataframe('5m', From)
    #             zScore = Zscore(df,20)[0]
    #             currentZscoreMA = CurrentzscoreMA(df,20)[0]
    #             currentPrice = df.iloc[-1].loc['colonne1']


    # plt.plot(Selecttime(start, end), LzScore)
    # plt.plot(Selecttime(start, end), LzScoreMA)
    # print(dataframe6mois1m.loc[55340:55400,'price'])

    Winrate = (Winrate/nombreDeTrade) * 100
    print("nombre de trade: " + str(nombreDeTrade))
    print("gain moyen par trade: " + str(Gainmoyentrade/nombreDeTrade))
    print("Winrate: " + str(Winrate) + "%")
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(Selecttime(dataframe6mois5m,start, end), LCapital)
    ax2.plot(Lindex,Lprice)
    plt.show()


# a = input("Entrez nom_du_fichier.json : ")
# b = input("backtestet ? (True or False) : ")
# debut = int(input("indice du début de 0 à 53200 : "))
# fin = int(input("indice de fin, doit être supérieur à indice de début : "))
# asyncio.run(main(a,b,debut,fin))

asyncio.run(main('essai.json' ,'True',100,67000))

# print(STD)
# print(displacement)
# def zScore(asset,timeframe):
#    curentMA
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
    if backtest == True:
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


# dataframe pour 6 mois en 5 miutes pour backtester



# Dans les lignes suivantes on ouvre un fichier et on écrit du json dedans mais pas besoin
# with open('btc_bars.json', 'w') as e:
#     json.dump(klines, e)
# Pour plot : 
def plot(x,y1,y2):
    plt.plot(x, y1, color='r', label='zcore')
    plt.plot(x, y2, color='g', label='zscoreMA')
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


dataframe6mois5m = pd.read_pickle("./dataframe6mois5m.pkl")
dataframe6mois1m = pd.read_pickle("./dataframe6mois1m.pkl")
LCapital = [1000]
Lprice = []
Lindex = []
async def main(filename,backtest,start,end):
    file = open(filename, 'w+')
    entryTime = start
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable pour savoir si le zscore est au dessus de 3 ou en dessous de -3
    Bornes = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCours = False
    Capital = 1000
    if backtest == 'True':
        #On veut monitor le trade en cours donc dans le while, on va regarder le prix toutes les minutes
        Entryprice = 0
        currentPrice1m = 0
        currentZscoreMA1m = 0
        currentZscore1m = 0
        LzScore = [dataframe6mois5m.loc[start,'zscore']]
        LzScoreMA = [dataframe6mois5m.loc[start,'zscoreMA']]
        #Strategie va etre : sell when zscore < currentMA
        #Close trade when zscore = currentMA
        #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
        k = Decimal(start)
        while k < end:
            k+=Decimal(1)
            LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
            LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
            LCapital.append(Capital)
            if dataframe6mois5m.loc[int(k),'zscore'] >= 3:
                Bornes = 3
            if  dataframe6mois5m.loc[int(k),'zscore'] < dataframe6mois5m.loc[int(k),'zscoreMA'] and Bornes == 3 and dataframe6mois5m.loc[int(k-1),'zscore'] > dataframe6mois5m.loc[int(k),'zscore'] : 
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
                while dataframe6mois5m.loc[int(k),'zscore'] < dataframe6mois5m.loc[int(k),'zscoreMA'] and k<end and enCours: #currentZscore1m >= 0
                    #ici on passe sur la dataframe une minute
                    #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                    
                    index +=1
                    k = Decimal(str(k)) + Decimal('0.2')
                    Lindex.append(dataframe6mois1m.loc[index,'date'])
                    Lprice.append(dataframe6mois1m.loc[index,'price'])
                    # print(dataframe6mois1m.loc[index, ['price','date']])
                    if Decimal(str(k))%1 == 0.0:
                        LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
                        LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
                        LCapital.append(Capital)
                    if (Entryprice-dataframe6mois1m.loc[index,'price'])/Entryprice > 0.005:
                        enCours = False
                        break
                    if (dataframe6mois1m.loc[index,'price']-Entryprice)/Entryprice > 0.003:
                        enCours = False
                        break

                outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
                Outprice = dataframe6mois1m.loc[index,'price']
                #Donc faut arreter le backtesting si le capital tombe à 0 
                Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
                Capital = Capital + Resultattrade
                nombreDeTrade+=1
                ClosedTrade = {'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
                with open(filename, 'a+') as e:
                    json.dump(ClosedTrade, e)
                if not Decimal(str(k))%1 == 0.0:
                    k = Decimal(ceil(k))
                    currentPrice = dataframe6mois5m.loc[int(k),'price']
                    currentZscoreMA = dataframe6mois5m.loc[int(k),'zscoreMA']
                    currentZscore = dataframe6mois5m.loc[int(k),'zscore']
                    LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
                    LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
                    LCapital.append(Capital)
    else:    

        #a update dans la boucle
        now = int( time.time() )*1000
        From = now - 14400000
        df = dataframe('5m', From)
        zScore = Zscore(df,20)[0]
        currentZscoreMA = CurrentzscoreMA(df,20)[0]
        currentPrice = df.iloc[-1].loc['colonne1']
        Entryprice = 0
        #Strategie va etre : sell when zscore < currentMA
        #Close trade when zscore = currentMA
        #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
        while TRUE:
            print(zScore, currentZscoreMA)
            if zScore < currentZscoreMA:
                Entryprice = currentPrice
                while zScore < currentZscoreMA:
                    await asyncio.sleep(300)
                    #On update dans la boucle toutes les 5 min pour avoir les dernieres données 
                    now = int( time.time() )*1000
                    From = now - 14400000
                    df = dataframe('5m', From)
                    zScore = Zscore(df,20)[0]
                    currentZscoreMA = CurrentzscoreMA(df,20)[0]
                    currentPrice = df.iloc[-1].loc['colonne1']
                    print(zScore, currentZscoreMA)
                Outprice = currentPrice
                Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
                Capital = Capital + Resultattrade
                ClosedTrade = {'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital }
                print("trade done !")
                with open(filename, 'a+') as e:
                    json.dump(ClosedTrade, e)
            else:
                
                await asyncio.sleep(300)
                now = int( time.time() )*1000
                From = now - 14400000
                df = dataframe('5m', From)
                zScore = Zscore(df,20)[0]
                currentZscoreMA = CurrentzscoreMA(df,20)[0]
                currentPrice = df.iloc[-1].loc['colonne1']
    # plt.plot(Selecttime(start, end), LzScore)
    # plt.plot(Selecttime(start, end), LzScoreMA)
    # print(dataframe6mois1m.loc[55340:55400,'price'])
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(Selecttime(dataframe6mois5m,start, end), LCapital)
    ax2.plot(Lindex,Lprice)
    # plt.plot(Selecttime(dataframe6mois5m,start, end), LCapital)
    plt.show()
# a = input("Entrez nom_du_fichier.json : ")
# b = input("backtestet ? (True or False) : ")
# debut = int(input("indice du début de 0 à 53200 : "))
# fin = int(input("indice de fin, doit être supérieur à indice de début : "))
# asyncio.run(main(a,b,debut,fin))
asyncio.run(main('essai.json' ,'True',300,53100))

# print(STD)
# print(displacement)
# def zScore(asset,timeframe):
#    curentMA
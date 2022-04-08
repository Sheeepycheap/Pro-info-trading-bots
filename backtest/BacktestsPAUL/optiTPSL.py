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



# dataframe6mois5m = pd.read_pickle("./dataframe6mois5m.pkl")
# dataframe6mois1m = pd.read_pickle("./dataframe6mois1m.pkl")

dataframe6mois5m = pd.read_pickle("./dataframe6mois5mETH.pkl")
dataframe6mois1m = pd.read_pickle("./dataframe6mois1mETH.pkl")

LCapital = [1000]
Lprice = []
Lindex = []
L = []
LTP = []
LSL = []
Lcapital = []
async def main(filename,backtest,start,end):
    TP = Decimal('0.01')
    SL = Decimal('0.001')
    Capitaltest = 0
    couple = [TP,SL, Capitaltest]
    file = open(filename, 'w+')
    entryTime = start
    typetrade = 'long'
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable pour savoir si le zscore est au dessus de 3 ou en dessous de -3
    Bornes = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCours = False
    Capital = 1000
    if backtest == 'True':
        #On veut monitor le trade en cours donc dans le while, on va regarder le prix toutes les minutes

        #On va essayer d'optimiser les Tps et SL pour la stratégie:

        while TP < 0.02:
            TP += Decimal('0.0005')
            SL = Decimal('0.001')
            while SL < TP/2 + TP/5:
                SL += Decimal('0.0005')
                Capital = 1000
                Entryprice = 0
                LzScore = [dataframe6mois5m.loc[start,'zscore']]
                LzScoreMA = [dataframe6mois5m.loc[start,'zscoreMA']]

                #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
                k = Decimal(start)
                while k < end:
                    k+=Decimal(1)
                    # LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
                    # LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
                    # LCapital.append(Capital)
                    if dataframe6mois5m.loc[int(k)-1,'zscore'] >= 2.4 and dataframe6mois5m.loc[int(k),'zscore'] < dataframe6mois5m.loc[int(k) - 1, 'zscore']:
                        Bornes = 1
                    if  dataframe6mois5m.loc[int(k)-1,'zscore'] <= -2.4 and dataframe6mois5m.loc[int(k),'zscore'] > dataframe6mois5m.loc[int(k) - 1, 'zscore']:
                        Bornes = -1
                        
                    #Short condition
                    if Bornes == -1 :
                        typetrade = 'short'
                        # print('entrée dans trade')
                        Bornes = 0 
                        Entryprice = dataframe6mois5m.loc[int(k),'price']
                        entryTimestamp = dataframe6mois5m.loc[int(k),'date']
                        entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                        #on initialise les datas pour la timeframe 1m
                        index = dataframe6mois1m.loc[dataframe6mois1m['date'] == entryTimestamp+240,'price'].index[0]
                        # Lindex.append(dataframe6mois1m.loc[index,'date'])
                        # Lprice.append(dataframe6mois5m.loc[int(k),'price'])
                        enCours = True
                        # while enCours:
                        while dataframe6mois5m.loc[int(k)-1,'zscore'] < 2.4 and k<end or enCours and k < end:
                            #ici on passe sur la dataframe une minute
                            #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                            
                            index +=1
                            k = Decimal(str(k)) + Decimal('0.2')
                            # Lindex.append(dataframe6mois1m.loc[index,'date'])
                            # Lprice.append(dataframe6mois1m.loc[index,'price'])
                            # print(dataframe6mois1m.loc[index, ['price','date']])
                            # if Decimal(str(k))%1 == 0.0:
                            #     LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
                            #     LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
                            #     LCapital.append(Capital)
                            if (dataframe6mois1m.loc[index,'price']-Entryprice)/Entryprice > TP:
                                enCours = False
                                break
                            if (Entryprice - dataframe6mois1m.loc[index,'price'])/Entryprice > SL:
                                enCours = False
                                break

                        # outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')

                        # #Donc faut arreter le backtesting si le capital tombe à 0
                        Outprice = dataframe6mois1m.loc[index,'price']
                        Resultattrade = Capital * (Outprice - Entryprice)/Entryprice
                        Capital = Capital + Resultattrade
                        # nombreDeTrade+=1
                        # ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
                        # with open(filename, 'a+') as e:
                        #     json.dump(ClosedTrade, e)
                        if not Decimal(str(k))%1 == 0.0:
                            k = Decimal(ceil(k))
                            # LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
                            # LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
                            # LCapital.append(Capital)
                LTP.append(float(TP))
                LSL.append(float(SL))
                Lcapital.append(float(Capital))
                L.append([float(TP),float(SL),Capital])
                if Capital > Capitaltest:
                    Capitaltest = Capital 
                    couple = [float(TP), float(SL), Capitaltest]

        fichier = open("data.txt", "w")
        fichier.write(str(L))
        fichier.close()
        print(couple)
        fig = plt.figure(figsize=(0.024,0.024,))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs = LTP, ys = LSL, zs = Lcapital)
        plt.show()



# a = input("Entrez nom_du_fichier.json : ")
# b = input("backtestet ? (True or False) : ")
# debut = int(input("indice du début de 0 à 53200 : "))
# fin = int(input("indice de fin, doit être supérieur à indice de début : "))
# asyncio.run(main(a,b,debut,fin))

asyncio.run(main('essai.json' ,'True',58000,59000))
# 60960
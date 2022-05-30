from pickle import TRUE
from pandas import *
import pandas as pd
import yfinance as yf
import requests as rq
from binance import *
import asyncio
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from math import *
from decimal import *
import automatisationbacktest as aut


def Selecttime(dataframe,startime, endtime):
    Lx = []
    for k in range(startime,endtime+1):
        
        Lx.append(dataframe.loc[k,'date'])
    return Lx

#importation des dataframe pour le backtest:
dataframe6mois5m = pd.read_pickle("./dataframe1.5mois5mBTCUSDT")
dataframe6mois1m = pd.read_pickle("./dataframe9.3mois1mBTCUSDT")

#Initialisation de liste pour différentes représenations graphiques
LCapital = []
Lprice = []
Lindex = []
async def main(filename,backtest,start,end):
    #Valeurs de TP/SL pour la stratégie (a adapter en fonction de la stratégie à bakctester)
    TP = 0.0165
    SL = 0.0012
    file = open(filename, 'w+')
    entryTime = start
    typetrade = 'long'
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable pour utile dans certaines stratégies
    Bornes = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCours = False
    #On initialise le capital de départ à 1000
    Capital = 1000
    longpossibility = False
    shortpossibility = False
    if backtest == 'True':

        Gainmoyentrade = 0 
        Winrate = 0
        k = Decimal(start)
        #On instancie un objet backtest avec les données acutelles, elles seront modifiées à chaques entré dans un trade
        back1 = aut.backtest(dataframe6mois5m, dataframe6mois1m, filename,\
        TP, SL, k, end , enCours, Capital, nombreDeTrade, Winrate, Gainmoyentrade, Lindex ,Lprice, LCapital)

        #On parcourt toute la dataframe
        while k < end:
            """"
            On parcourt toute la dataframe

            A chaque étape on change les variables essentiels dans le backtesting (puisqu'elles sont différentes pour tout k). 
            Ici on peut initialiser des conditions pour ouvrir des shorts et des longues, enfaite on va définir la stratégie à backtester
            
            Toutes les valeurs numériques sont changeable, elles sont choisis car c'est celles qui donnent les meilleurs rendement mais  
            il peut en exister des meilleurs

            /!\ Si du code est commenté c'est qu'il est souvent utile mais pas dans le dernier cas testé. 
            """

            k+=Decimal(1)

            #Ici on met à jour les informations importantes dans le backtest à chaque itération
            back1.updateL(back1.Capital,dataframe6mois5m.loc[int(k),'date'],dataframe6mois5m.loc[int(k),'price'])

            
            """ Code commenté utile dans certaines stratégies"""
            # if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3: #Ici code pour startégie zscore
            #     shortpossibility = True
            # elif dataframe6mois5m.loc[int(k),'20Zscore_price'] <= 1:
            #     shortpossibility = False
            # if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3 :
            #     longpossibility = True
            # elif dataframe6mois5m.loc[int(k),'20Zscore_price'] >= -1:
            #     longpossibility = False
            """ Fin Code commenté utile dans certaiens stratégies"""

            #On définit les entrées dans un trade (entrée long =/= de entréé short)
            Entryconditionshort = dataframe6mois5m.loc[int(k-1), '20Zscore_price'] > 2.4 and dataframe6mois5m.loc[int(k-1), '20Zscore_price'] > dataframe6mois5m.loc[int(k), '20Zscore_price']
            Entryconditionlong = False
            #Si les conditions précédentes sont réalisées alors on rentre dans un trade et on entre aussi dans la partie automatique du backetesting
            #la base de donnée va etre parcouru à la recherche d'une condition de sortie
            #L'inconvenient c'est que les conditions de sorties outre TP et SL doivent etre mentionner dans automatisaiont_backtest() avant le début du bakctest
            #
            if Entryconditionshort and not Entryconditionlong:
                typetrade = 'short'
                #Il faut ici changer la timeframe en fonction de sur quelle timeframe est la stratégie principale. 
                back1.automatisation_backtest(TP , SL, typetrade, Entryconditionshort, Entryconditionlong, k, enCours, '15m', Lindex, Lprice, LCapital, True)
                k = back1.indice
            
            if Entryconditionlong and not Entryconditionshort:
                typetrade = 'long'
                back1.automatisation_backtest(TP , SL, typetrade, Entryconditionlong, Entryconditionlong, k, enCours, '15m', Lindex, Lprice, LCapital)
                k = back1.indice
                longpossibility = False
                
#sauvegarde de variables utiles pour juger de la viabilité d'une stratégie
    Winrate = (back1.Winrate / back1.nombreDeTrade) * 100
    print("nombre de trade: " + str(back1.nombreDeTrade))
    print("gain moyen par trade: " + str(back1.Gainmoyentrade/back1.nombreDeTrade))
    print("Winrate: " + str(Winrate) + "%")
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(Lindex, back1.LCapital)
    ax2.plot(Lindex,Lprice)
    plt.show()


a = input("Entrez nom_du_fichier.json : ")

debut = int(input("Faire le choix de l'indice de début (de 0 à " + str(len(dataframe6mois5m)) + " ) : "))
fin = int(input("Faire le choix de l'indice de fin, doit être supérieur à indice de début et inférieur à " + str(len(dataframe6mois5m)) + " : "))


asyncio.run(main(a ,'True',debut,fin))


""""

Ici on sauvegarde du code utile pour le backteste d'ancienne stratégie
On a donc des exemples de code intéréssant et réutilisable

"""
#
#cas du bot stratégie 1 
#
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3:
#    shortpossibility = True
#if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3:
#    longpossibility = True
#Entryconditionshort = shortpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1, '20Zscore_price'] and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k), '20SMA_20Zscore_price']
#Entryconditionlong = longpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1, '20Zscore_price'] and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k), '20SMA_20Zscore_price']

#
#Cas du bot stratégie 2 
#
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3:
#     shortpossibility = True
# elif dataframe6mois5m.loc[int(k),'20Zscore_price'] <= 1:
#     shortpossibility = False
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3 :
#     longpossibility = True
# elif dataframe6mois5m.loc[int(k),'20Zscore_price'] >= -1:
#     longpossibility = False
# Entryconditionshort = dataframe6mois5m.loc[int(k),'7SMA_price'] >= dataframe6mois5m.loc[int(k),'20SMA_price'] and shortpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1,'20Zscore_price']
# Entryconditionlong = dataframe6mois5m.loc[int(k),'7SMA_price'] <= dataframe6mois5m.loc[int(k),'20SMA_price'] and longpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1,'20Zscore_price']
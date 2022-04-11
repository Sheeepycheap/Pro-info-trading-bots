from pyparsing import col
import yfinance as yf 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import MetaTrader5 as mt5 

def ydataframe(stock : str, start : str , interval : str ) -> pd.DataFrame :
    # ""
    # permet d'obtenir une dataframe issue de yfinance rapidement sans prise de tête. Le problème est que
    # yfinance fournie des dataframes limitées en terme de données ( pour des interval de 5m, on ne peut
    # pas dépasser 60 jours par exemple). Pour du backtest, il faut importer la data manuellement, mais 
    # pour du live trading, cela suffit. 
    # ""

    df = yf.download(stock,start = start, interval=interval )
    df.dropna(inplace=True)
    return df

def ema(data, length : str, column : str ) -> pd.DataFrame :
    #""
    #rajoute la colonne des ema d'une colonne. L'ema se calcul sur length unités. Renvoie une dataframe.
    #""
    data[str(length) + "EMA_" + column] = data[column].ewm(span = length , adjust = False).mean()

def sma(data,length : str, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des sma d'une colonne. Le sma se calcul sur length unités. Renvoie une dataframe.
    #""    
    data[str(length) + "SMA_" + column] = data[column].rolling(window=length).mean()

def std(data, length : int, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des std d'une colonne. Le std se calcul sur length unité. Renvoie une dataframe.
    #""
    data[str(length) + "STD_" + column] = data[column].rolling(window=length).std()

def zscore(data, length : int, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des zscore d'une colonne. Le zscore se calcul sur le length unité. Renvoie une datafram
    #Le zscore se calcul en trois étapes
    #""
    sma(data,length, column)
    displacement = data[column] - data[str(length) + "SMA_" + column]
    std(data, length, column)
    data[str(length) + "Zscore_" + column] = displacement.divide(data[str(length) + "STD_" + column])

def quantile(data, length : int, column : str, q : int) -> pd.DataFrame:
    #""
    #rajoute la colonne des quantile d'une colonne. Le quantile se calcul sur length unité. Renvoie une dataframe.
    #""
    data[str(length) + "QUANT_" + str(q) + "_" + column] = data[column].rolling(window = length).quantile(q)
def variation(data, variationrange : int, column : str) -> pd.DataFrame:
    #""
    #Calcule la colonne des valeurs absolues des variations par rapport à une valeur précédente d'une colonne. 
    #Renvoie une dataframe consitué d'une unique colonne qui contient les variations.
    #""
    intermediarydataframe = data[column].iloc[variationrange:].reset_index(drop = True)
    return (data[column] - intermediarydataframe).abs()

def smoothaveragerange(data, column : str, fastperiod : float, fastrange : float) -> pd.DataFrame:
        wper = fastperiod*2 - 1
        smr = variation(data, 1, column).ewm(span =  fastperiod , adjust = False).mean()

        return smr.ewm(span = wper, adjust = False).mean()*fastrange

  

def removekey(orders) : 
    #""
    # Permet de supprimer la key "position" de orders. Pour ouvrir un ordre, il faut fournir un dictionnaire orders (qui ne contient pas 
    # de key "position"). Or si orders contient une key 'position', et bien il faut l'enlever pour pouvoir passer la transaction.
    #""
    orders.pop("position")
    return orders

def addkey(orders, position : int) :
    #""
    # Permet d'ajouter la key "position" de orders. Pour fermer une position, il faut fournir un dictionnaire orders (qui contient 
    # une key "position"). Or si orders ne contient pas une key 'position', et bien il faut l'ajouter pour pouvoir passer la transaction.
    #""
    orders['position'] = position
    return position

def money_to_volume(market: str, money : float) -> float :
    #""
    # Permet de convertir un nombre float représentant l'argent que l'on souhaite placer dans un actif en volume. Dans orders, Mt5 ne comprend
    # que 'volume' pour connaître le montant à placer dans une opération, or volume dépend du prix de l'actif mis en jeu. Si on veut placer 
    # 2000 euros sans se soucier de combien ça représente en volume de l'actif, on utilise cette fonction. 
    #""
    prix_1market = mt5.symbol_info_tick(market).ask
    return round(money/prix_1market,2)

def SAR(data):
    #""
    #rajoute la colonne des sar d'une colonne. L'ema se calcul sur length unités. Renvoie une dataframe.
    #Pour cela on va avoir besoin de la colonner des AF (acceleration factor) qui sont des valeurs permettant de juger l'évolution
    #de la tendance AF0 = 0.02 et si on fait un nouveau plus haut (resp plus bas) alors AF += 0.02 et max(AF) = 0.2
    #EP = extreme point, le plus haut (resp plus bas) de la tendance actuelle
    #On calcul le SAR à temps N avec la formule de récurence suivante: 
    #SARn = SAR(n-1) + AF(n-1)*(EP(n-1) - SAR(n-1)) sachant que SAR(0) = 1 er high (resp low) de la tendance haussière (resp baissière)
    #""
    data['AF'] = np.nan
    data['PSAR'] = np.nan
    data['EP'] = np.nan
    data['PSARdir'] = np.nan

    data.loc[0, 'AF'] = 0.02
    data.loc[0, 'PSAR'] = data.loc[0, 'low']
    data.loc[0, 'EP'] = data.loc[0, 'high']
    data.loc[0, 'PSARdir'] = "uptrend"

    for a in range(1, len(data)):

        if data.loc[a-1, 'PSARdir'] == 'uptrend':

            data.loc[a, 'PSAR'] = data.loc[a-1, 'PSAR'] + (data.loc[a-1, 'AF']*(data.loc[a-1, 'PSAR']-data.loc[a-1, 'EP']))            

            data.loc[a, 'PSARdir'] = "uptrend"

            if data.loc[a, 'low'] < data.loc[a-1, 'PSAR']:
                data.loc[a, 'PSARdir'] = "bear"
                data.loc[a, 'PSAR'] = data.loc[a-1, 'EP']
                data.loc[a, 'EP'] = data.loc[a-1, 'low']
                data.loc[a, 'AF'] = .02

            else:
                if data.loc[a, 'high'] > data.loc[a-1, 'EP']:
                    data.loc[a, 'EP'] = data.loc[a, 'high']
                    if data.loc[a-1, 'AF'] <= 0.18:
                        data.loc[a, 'AF'] =data.loc[a-1, 'AF'] + 0.02
                    else:
                        data.loc[a, 'AF'] = data.loc[a-1, 'AF']
                elif data.loc[a, 'high'] <= data.loc[a-1, 'EP']:
                    data.loc[a, 'AF'] = data.loc[a-1, 'AF']
                    data.loc[a, 'EP'] = data.loc[a-1, 'EP']               



        elif data.loc[a-1, 'PSARdir'] == 'bear':

            data.loc[a, 'PSAR'] = data.loc[a-1, 'PSAR'] - (data.loc[a-1, 'AF']*(data.loc[a-1, 'PSAR']-data.loc[a-1, 'EP']))

            data.loc[a, 'PSARdir'] = "bear"

            if data.loc[a, 'high'] > data.loc[a-1, 'PSAR']:
                data.loc[a, 'PSARdir'] = "uptrend"
                data.loc[a, 'PSAR'] = data.loc[a-1, 'EP']
                data.loc[a, 'EP'] = data.loc[a-1, 'high']
                data.loc[a, 'AF'] = .02

            else:
                if data.loc[a, 'low'] < data.loc[a-1, 'EP']:
                    data.loc[a, 'EP'] = data.loc[a, 'low']
                    if data.loc[a-1, 'AF'] <= 0.18:
                        data.loc[a, 'AF'] = data.loc[a-1, 'AF'] + 0.02
                    else:
                        data.loc[a, 'AF'] = data.loc[a-1, 'AF']

                elif data.loc[a, 'low'] >= data.loc[a-1, 'EP']:
                    data.loc[a, 'AF'] = data.loc[a-1, 'AF']
                    data.loc[a, 'EP'] = data.loc[a-1, 'EP']           










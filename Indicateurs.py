from pyparsing import col
import yfinance as yf 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import MetaTrader5 as mt5 
import talib 

def ydataframe(stock : str, start : str , interval : str ) -> pd.DataFrame :
    # ""
    # permet d'obtenir une dataframe issue de yfinance rapidement sans prise de tête. Le problème est que
    # yfinance fournie des dataframes limitées en terme de données ( pour des interval de 5m, on ne peut
    # pas dépasser 60 jours par exemple). Pour du backtest, il faut importer la data manuellement, mais 
    # pour du live trading, cela suffit. 
    # ""
    df = yf.download(tickers = stock,start = start, interval=interval )
    df.dropna(inplace=True)
    return df

def slice_data(df,slice:int) -> pd.DataFrame :
    #""
    # Si on veut des dataframe de slice heures, on utilise cette fonction. Il n'y a pas de timeframe de 4h dans la 
    # librairie yfinance, donc il faut la construire. 
    #""
    num= []
    for k in range(1,len(df)+1) :
        num.append(k)
    df['index'] = num
    df = df[df['index'] % slice == 0]
    df = df.drop('index', 1)
    return df

def ema(data, length : int, column : str ) -> pd.DataFrame :
    #""
    #rajoute la colonne des ema d'une colonne. L'ema se calcul sur length unités. Renvoie une dataframe.
    #""
    data[str(length) + "EMA_" + column] = data[column].ewm(span = length , adjust = False).mean()
    return data

def sma(data,length : int, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des sma d'une colonne. Le sma se calcul sur length unités. Renvoie une dataframe.
    #""    
    data[str(length) + "SMA_" + column] = data[column].rolling(window=length).mean()
    return data

def std(data, length : int, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des std d'une colonne. Le std se calcul sur length unité. Renvoie une dataframe.
    #""
    data[str(length) + "STD_" + column] = data[column].rolling(window=length).std()
    return data

def zscore(data, length : int, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des zscore d'une colonne. Le zscore se calcul sur le length unité. Renvoie une datafram
    #Le zscore se calcul en trois étapes
    #""
    sma(data,length, column)
    displacement = data[column] - data[str(length) + "SMA_" + column]
    std(data, length, column)
    data[str(length) + "Zscore_" + column] = displacement / data[str(length) + "STD_" + column]     
    return data

def quantile(data, length : int, column : str, q : int) -> pd.DataFrame:
    #""
    #rajoute la colonne des quantile d'une colonne. Le quantile se calcul sur length unité. Renvoie une dataframe.
    #""
    data[str(length) + "QUANT_" + str(q) + "_" + column] = data[column].rolling(window = length).quantile(q)
    return data
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


def PSAR(df, af=0.02, max=0.2):
    #""
    #rajoute la colonne des sar d'une colonne. L'ema se calcul sur length unités. Renvoie une dataframe.
    #Pour cela on va avoir besoin de la colonner des AF (acceleration factor) qui sont des valeurs permettant de juger l'évolution
    #de latendance AF0 = 0.02 et si on fait un nouveau plus haut (resp plus bas) alors AF += 0.02 et max(AF) = 0.2
    #EP = extreme point, le plus haut (resp plus bas) de la tendance actuelle
    #On calcul le SAR à temps N avec la formule de récurence suivante: 
    #SARn = SAR(n-1) + AF(n-1)*(EP(n-1) - SAR(n-1)) sachant que SAR(0) = 1 er high (resp low) de la tendance haussière (resp baissière)
    #""
    df.loc[0, 'AF'] = 0.02
    df.loc[0, 'PSAR'] = df.loc[0, 'low']
    df.loc[0, 'EP'] = df.loc[0, 'high']
    df.loc[0, 'PSARdir'] = "bull"
    for a in range(1, len(df)):
        if df.loc[a-1, 'PSARdir'] == 'bull':
            df.loc[a, 'PSAR'] = df.loc[a-1, 'PSAR'] + df.loc[a-1,'AF']*(df.loc[a-1, 'EP']-df.loc[a-1, 'PSAR'])
            if df.loc[a, 'high'] > df.loc[a-1, 'EP']:
                df.loc[a,'EP'] = df.loc[a, 'high']
                if df.loc[a-1, 'AF'] <0.2:
                    df.loc[a, 'AF'] = df.loc[a-1, 'AF'] + af
                else:
                    df.loc[a, 'AF'] = df.loc[a-1, 'AF']
            else:
                df.loc[a,'EP'] = df.loc[a-1, 'EP']
                df.loc[a, 'AF'] = df.loc[a-1, 'AF']

            if df.loc[a-1, 'PSAR'] > df.loc[a,'low'] : 
                df.loc[a, 'PSARdir'] = 'bear'
                df.loc[a,'EP'] = df.loc[a, 'low']
                df.loc[a, 'AF'] = af
                if df.loc[a, 'high'] > df.loc[a-1, 'EP']:
                    df.loc[a, 'PSAR'] = df.loc[a, 'high']
                else:
                    df.loc[a, 'PSAR'] = df.loc[a-1,'EP']
            else:
                df.loc[a, 'PSARdir'] = 'bull'
        if df.loc[a-1, 'PSARdir'] == 'bear':
            df.loc[a, 'PSAR'] = df.loc[a-1, 'PSAR'] - df.loc[a-1,'AF']*(df.loc[a-1, 'PSAR'] - df.loc[a-1, 'EP'])
            if df.loc[a, 'low'] < df.loc[a-1, 'EP']:
                df.loc[a,'EP'] = df.loc[a, 'low']
                if df.loc[a-1, 'AF'] <0.2:
                    df.loc[a, 'AF'] = df.loc[a-1, 'AF'] + af
                else:
                    df.loc[a, 'AF'] = df.loc[a-1, 'AF']
            else:
                df.loc[a,'EP'] = df.loc[a-1, 'EP']
                df.loc[a, 'AF'] = df.loc[a-1, 'AF']
            if df.loc[a-1, 'PSAR'] < df.loc[a,'high'] : 
                df.loc[a, 'PSARdir'] = 'bull'
                df.loc[a,'EP'] = df.loc[a, 'high']
                df.loc[a, 'AF'] = af
                if df.loc[a, 'low'] < df.loc[a-1, 'EP']:
                    df.loc[a,'PSAR'] = df.loc[a, 'low']
                else:
                    df.loc[a, 'PSAR'] = df.loc[a-1,'EP']
            else:
                df.loc[a, 'PSARdir'] = 'bear'


def KijunLine(data : pd.DataFrame, colum : str ):
    data['kijun'] = (1/2) * ( data['high'].rolling(window = 26).max() + data['low'].rolling(window= 26).min())

def KijunLine(data : pd.DataFrame, colum : str ):
    data['tenkan'] = (1/2) * ( data['high'].rolling(window = 9).max() + data['low'].rolling(window= 9).min())

def reco_morningstar(data)-> pd.DataFrame: 
    #""
    # Ajoute une colonne Morningstar à la dataframe data. De manière générale, un chiffre positif supérieur (stricte) à 0 
    # signifie une détection d'une figure de retournement bullish et inversement si c'est négatif (stricte). 0 signifie
    # qu'il n'y a rien à signaler. 
    #""
    data['Morningstar'] = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
    return data

def reco_eveningstar(data)-> pd.DataFrame: 
    data['Eveningstar'] = talib.CDLEVENINGSTAR(data['Open'],data['High'], data['Low'], data['Close'] )
    return data

def RSI(data,length) -> pd.DataFrame :
    #""
    # Ajoute une colonne RSI. 
    #""
    data['RSI'] = talib.RSI(data['Close'], timeperiod=length)
    return data

def SAR(data)->pd.DataFrame : 
    #""
    # Ajoute une colonne SAR. 
    #""
    data['SAR'] = talib.SAR(data['High'], data['Low'], acceleration=0.02, maximum=0.2)
    return data

def MACD(df) -> pd.DataFrame : 
    #""
    # Ajoute une colonne MACD, Signal, et l'historigramme. 
    #""
    df['MACD'],df['Signal'],df['Hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df 




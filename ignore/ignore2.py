import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5 
import yfinance as yf
import pandas as pd

# login = 1
# password = "2"
# server = "2"
# if not mt5.login(login,password,server) :
#      messagebox.showerror("Identifiants incorrects","Vérifiez vos identifiants.")
# else :
#     print("ok")
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

def sma(data,length : str, column : str) -> pd.DataFrame:
    #""
    #rajoute la colonne des sma d'une colonne. Le sma se calcul sur length unités. Renvoie une dataframe.
    #""    
    data[str(length) + "SMA_" + column] = data[column].rolling(window=length).mean()
df = ydataframe(stock = "MSFT", start ='2022-02-14',interval='1d')
sma(data = df,length=20,column='Close')
print(df.dropna())


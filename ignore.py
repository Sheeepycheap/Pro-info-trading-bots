import time
import MetaTrader5 as mt5
import Indicateurs as ind
import matplotlib.pyplot as plt 
import yfinance as yf
import talib as tab

df = ind.ydataframe(stock = "BTC-USD", start = '2021-09-09', interval='1h')
#ind.zscore(df,length=20,column='Close')
# print(df[df['20Zscore_Close'] > 2.4 ])
ind.reco_morningstar(df)
ind.RSI(df, length=9)
print(df[df['Morningstar'] == 100] )
# data = df[df['RSI'] < 20] 
# print(data[data['Morningstar'] == 100 ])
op = False
achat = []
vente = []
for i in range (len(df)) :
    if  df['Morningstar'][i] == 100 and df['RSI'] > 60 and op == False :
        achat.append(df['Close'][i])
        op= True
        sl = df['Close'][i] - 0.01*df['Close'][i]
        tp = df['Close'][i] + 0.025*df['Close'][i]
    elif op == True and df['Close'][i] > tp : 
        vente.append(df['Close'][i])
        op = False
    elif op == True and df['Close'][i] <= sl :
        vente.append(df['Close'][i])
        op = False 

print(achat,vente)
def pv(list1,list2) :
    res = []
    if len(list1)>len(list2) :
        for i in range(0,len(list2)) :
            res.append(((list2[i] - list1[i])/list1[i]))
    if len(list1)<len(list2) :
        for i in range(0,len(list1)) :
            res.append(((list2[i] - list1[i])/list1[i]))           
    if len(list1) == len(list2) :
        for i in range(0,len(list1)) :
            res.append(((list2[i] - list1[i])/list1[i]))
    return res 
    

def resultat(n,res) :
    x = n
    for i in range(1,len(res)):
        x= x + x*res[i]
    return x

res = pv(achat,vente)
print(resultat(10000,res))




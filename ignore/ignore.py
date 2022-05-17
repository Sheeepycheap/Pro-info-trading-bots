import time
import MetaTrader5 as mt5
from pyparsing import col
import Indicateurs as ind
import matplotlib.pyplot as plt 
import yfinance as yf
import talib as tab

df = ind.ydataframe(stock = "BTC-USD", start = '2020-09-09', interval='1h')
ok = []
for k in range(1,len(df)+1) :
    ok.append(k)
df['num'] = ok
df = df[df['num'] % 4 == 0]
df = df.drop('num', 1)
print(df)
# ind.ema(df,length = 4,column='Close')
# ind.ema(df,length=9,column='Close')
# ind.ema(df,length=18,column='Close')
ind.reco_morningstar(df)
ind.RSI(df, length=9)
df['Eveningstar'] = tab.CDLEVENINGSTAR(df['Open'],df['High'], df['Low'], df['Close'] ) 
#print(df[df['Morningstar'] == 100])
#print(df[df['Eveningstar'] == -100])
# data = df[df['RSI'] < 50] 
# print(data[data['Morningstar'] == 100 ])
op = False
achat = []
vente = []
for i in range (len(df)) :
    if  df['Morningstar'][i] == 100   and op == False :
        achat.append(df['Close'][i])
        op= True
        sl = df['Close'][i] - 0.001*df['Close'][i]
        tp = df['Close'][i] + 0.02*df['Close'][i]
    elif op == True and df['Close'][i] > tp : 
        vente.append(df['Close'][i])
        op = False
    elif op == True and df['Close'][i] <= sl :
        vente.append(df['Close'][i])
        op = False 

op = False
achat1 = []
vente1 = []
for i in range (len(df)) :
    if  df['Eveningstar'][i] == -100  and op == False :
        achat1.append(df['Close'][i])
        op= True
        sl = df['Close'][i] + 0.001*df['Close'][i]
        tp = df['Close'][i] - 0.02*df['Close'][i]
    elif op == True and df['Close'][i] < tp : 
        vente1.append(df['Close'][i])
        op = False
    elif op == True and df['Close'][i] > sl :
        vente1.append(df['Close'][i])
        op = False 

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
    
def pv_short(list1,list2) :
    res = []
    if len(list1)>len(list2) :
        for i in range(0,len(list2)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))
    if len(list1)<len(list2) :
        for i in range(0,len(list1)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))           
    if len(list1) == len(list2) :
        for i in range(0,len(list1)) :
            res.append(((-1)*(list2[i] - list1[i])/list1[i]))
    return res 



def resultat(n,res) :
    x = n
    for i in range(1,len(res)):
        x= x + x*res[i]
    return x

res = pv(achat,vente) + pv_short(achat1,vente1)
# print(resultat(10000,res))








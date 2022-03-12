import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import yfinance as yf


# Part 1 : Get the datas 
#aapl = yf.Ticker('AAPL')
#df = aapl.history(period='1y')
df = yf.download( "ETH-USD",start = '2022-03-04', interval='1m')
df.dropna(inplace=True)
# Part 2 : show the Data 
plt.title('Cours de AAPL')
plt.plot(df.index,df['Close'])
plt.xlabel("Date")
plt.ylabel("Price")

# Part 3 : Calculate the EMAs 

df['5ema']=df['Close'].ewm(span = 4 , adjust = False).mean()
shortEMA= df['5ema']
df['60ema']=df['Close'].ewm(span = 18 , adjust = False).mean()
longEMA = df['60ema']
df['20ema']=df['Close'].ewm(span = 9 , adjust = False).mean()
MiddleEMA=df['20ema']
df.dropna(inplace=True)
print(df)

# Part 4 : show the EMAs 
plt.plot(shortEMA, label = "5ema", color ='violet')
plt.plot(longEMA, label="60ema",color = 'red')
plt.plot(MiddleEMA, label="20ema", color = 'orange')

# Part 5 buy and sell
def buy_sell(data) :
    buy=[]
    sell=[]
    test1=[]
    test2=[]
    # PositionSell determine la position dans laquelle où nous sommes : doit-on acheter ou vendre ?
    PositionSell = False # on est pas dans une position où l'on doit vendre avant de procéder à une autre action.
    for i in range (0, len(data)) :
        if data['5ema'][i] > data['20ema'][i] and data['20ema'][i]>data['60ema'][i] and  PositionSell == False :
            buy.append(data['Close'][i])
            PositionSell = True
            test1.append(data['Close'][i])
            sell.append(np.nan)
        elif PositionSell== True and  data['5ema'][i]<data['20ema'][i] and data['20ema'][i]<data['60ema'][i] :
            sell.append(data['Close'][i])
            test2.append(data['Close'][i])
            PositionSell= False
            buy.append(np.nan)
        else :
            sell.append(np.nan)
            buy.append(np.nan)
    return (buy,sell,test1,test2)
# Part 6 see the result
plt.scatter( df.index,buy_sell(df)[0], color='green' )
plt.scatter( df.index,buy_sell(df)[1], color='red' )

# Part 7 Voir la PV
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

res = pv(buy_sell(df)[2],buy_sell(df)[3])

print (resultat(10000,res))
plt.show()

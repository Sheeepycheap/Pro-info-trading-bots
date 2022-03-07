import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import yfinance as yf

# import des datas
df = yf.download('SOL-USD',start='2022-01-01',interval="5m")
#Calcul des sma et écart type
df['sma'] = df['Close'].rolling(window=20).mean()
df['ecart type'] = df['Close'].rolling(window=20).std()
# implémente le zscore et l'éma du zscore
def Zscore(data):
    diff = data['Close'] - data['sma']
    data['zscore']= diff / data['ecart type']
Zscore(df)
df['zscore ema']=df['zscore'].ewm(span = 20, adjust = False).mean()
df.dropna(inplace=True)
# enfin voilà la strat :    
openop =[]
closeop=[]
def strat_de_paul(data) : 
    no_op = True # a-t-on une opération en attente ? si c'est True ça veut dire qu'il n'y a pas d'ordre en attente d'être clôt 
                 # donc on peut procéder à une opération. C'est pour éviter d'ouvrir 2 positions à la fois 
    for i in range (len(data)) :  
        if data['zscore'][i] > data['zscore ema'][i] and data['zscore'][i-1] < data['zscore ema'][i-1] and no_op == False :
            closeop.append(data['Close'][i])
            no_op=True
        elif data['zscore'][i] >= 3 and no_op == True  :
            for j in range (i,len(data)):
                if data['zscore'][j] < data['zscore ema'][j] and data['zscore'][j-1] > data['zscore ema'][j-1]  :
                    no_op = False 
                    openop.append(data['Close'][j])
                    break 

# Cette statégie semble peut rentable , mais en faisant : on prend le short si zscore >=3 et on clôture 
# au premier croisement, on a de meilleur résultat ( à vérifier ). ça donne ça : 
#    def strat_de_paul(data) : 
#    no_op = True # a-t-on une opération en attente ? si c'est True ça veut dire qu'il n'y a pas d'ordre en attente d'être clôt 
#                # donc on peut procéder à une opération. C'est pour éviter d'ouvrir 2 positions à la fois 
#   for i in range (len(data)) :  
#       if data['zscore'][i] < data['zscore ema'][i] and data['zscore'][i-1] > data['zscore ema'][i-1] and no_op == False :
#            closeop.append(data['Close'][i])
#            no_op=True
#        elif data['zscore'][i] >= 3 and no_op == True  :
#             no_op = False 
#             openop.append(data['Close'][i])
            

strat_de_paul(df)

#là on fait que du backtest sur 2 mois, pour un début à 1000 (changer cap si on veut plus) :
cap=1000
res=[] # liste des plus-values des opérations.
def rendement(opp,cp) :
    if len(opp)>len(cp) :
        for i in range(0,len(cp)) :
            res.append(((-1)*(opp[i] - cp[i])/opp[i]))
    if len(opp)<len(cp) :
        for i in range(0,len(opp)) :
            res.append(((-1)*(opp[i] - cp[i])/opp[i]))           
    if len(opp) == len(cp) :
        for i in range(0,len(opp)) :
            res.append(((-1)*(opp[i] - cp[i])/opp[i]))

rendement(openop,closeop) #cette ligne c'est juste pour update res

# là c'est juste du plot. C'est pour avoir un visu
cap_aplot = [cap] #liste contenant le montant du capital (évolue au fur et à mesure)
def resultat(n,res) :
    x = n
    for i in range(1,len(res)):
        x= x + x*res[i]
        cap_aplot.append(x)
    return x

print("à la fin, on a :" + str(resultat(cap,res)))

p = [] # la prochaine option permet d'avoir l'axe x pour pouvoir plot. C'est juste une liste allant de 0 à len(res). A ignorer
for i in range (len(res)) :
    p.append(i)

# on plote tout ça : 
plt.title('capital')
plt.xlabel('opérations')
plt.ylabel('capital')
plt.scatter(p,cap_aplot)
plt.show()
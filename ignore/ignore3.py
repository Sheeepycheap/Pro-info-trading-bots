import time
import MetaTrader5 as mt5
import Indicateurs as ind
import matplotlib.pyplot as plt 
import yfinance as yf



def usr_login(usr : int, mdp : str, server : str) :
    if not mt5.initialize() : 
         print("MetaTrader5 n'a pas pu être initialisée")
         quit()
    else : 
        if not mt5.login(usr,mdp,server) : 
            print("Vérifiez vos identifiants")
        else : 
            print("Connexion réussie !")

usr_login(usr = 41600933, mdp = "ZL6HzUageSX6", server = "AdmiralMarkets-Demo" )


point = mt5.symbol_info("BTCUSD").point
print(point)
ask = mt5.symbol_info_tick("BTCUSD").ask
bid = mt5.symbol_info_tick("BTCUSD").bid
print(ask,bid)

prix = mt5.symbol_info_tick("BTCUSD").bid
print(prix)
sl = 0.0
tp = 0.0
print(sl,tp)
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "BTCUSD",
    "volume": 0.01,
    "type": mt5.ORDER_TYPE_SELL,
    "price": prix,
    "sl": sl,
    "tp": tp,
    "deviation": 20,
    "magic": 234000,
    "comment": "test",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

result = mt5.order_send(request)
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send a échoué, retcode={}".format(result.retcode))

time.sleep(2)
position = mt5.positions_get()[-1].ticket 
print(position)
sell = {
    "action" : mt5.TRADE_ACTION_DEAL,
    "symbol" : "BTCUSD",
    "volume" : 0.01,
    "type" : mt5.ORDER_TYPE_BUY,
    "price" : prix,
    "sl": 0.0,
    "tp": 0.0,
    "deviation": 20,
    "magic": 234000,
    "comment": "test",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    "position" : position
}

mt5.order_send(sell)
while True :
    prix = mt5.symbol_info_tick("BTCUSD").bid
    if prix <= sl :
        print("vends")
        mt5.order_send(sell)
        break
    elif prix >= tp : 
        print("vend mais avec pv")
        mt5.order_send(sell)
        break
    time.sleep(1)


    
print("fin")









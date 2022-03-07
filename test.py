from turtle import pos
import MetaTrader5 as mt5 

mt5.initialize()
print("ok")
login = 41552251
password = "ee4rli8A1iLU"
server = "AdmiralMarkets-Demo"
mt5.login(login,password,server)

print("ok")

#position = mt5.positions_get()[0]._asdict()['ticket']
#volume = mt5.positions_get()[0]._asdict()['volume']
orders = {
    "action" : mt5.TRADE_ACTION_DEAL ,  
    "symbol" : "BTCUSD" ,
    "volume" : "volume" ,
    "type" : mt5.ORDER_TYPE_SELL ,
    "price" : mt5.symbol_info_tick("BTCUSD").ask,
    "sl" : 0.0 ,
    "tp" : 0.0 ,
    "deviation" : 20 ,
    "magic" : 234000 ,
    "comment" : "test",
    "type_time" : mt5.ORDER_TIME_GTC,
    "type filling" : mt5.ORDER_FILLING_IOC, 
    'position' : "position",          
}

prix = mt5.symbol_info("BTCUSD").ask
print(prix)
account_info = mt5.account_info()
#mt5.order_send(orders)
#print(position)
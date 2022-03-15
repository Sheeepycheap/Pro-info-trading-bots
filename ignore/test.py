from turtle import pos
import MetaTrader5 as mt5 

mt5.initialize()

login = 41552251
password = "ee4rli8A1iLU"
server = "AdmiralMarkets-Demo"
if not mt5.login(login,password,server) :
    print("nope")


prix = mt5.symbol_info("BTCUSD")

print(prix)
position = mt5.positions_get()[-1].ticket
print(position)
volume = mt5.positions_get()[0].volume
print(volume)
orders = {
    "action" : mt5.TRADE_ACTION_DEAL ,  
    "symbol" : "BTCUSD" ,
    "volume" : volume ,
    "type" : mt5.ORDER_TYPE_SELL,
    "price" : mt5.symbol_info_tick("BTCUSD").ask,
    "sl" : 0.0 ,
    "tp" : 0.0 ,
    "deviation" : 20 ,
    "magic" : 234000 ,
    "comment" : "test",
    "type_time" : mt5.ORDER_TIME_GTC,
    "type filling" : mt5.ORDER_FILLING_IOC, 
    "position"  : position
}


#print(mt5.order_send(orders))
mt5.order_send(orders)

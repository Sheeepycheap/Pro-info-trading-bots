import bot
import MetaTrader5 as mt5


def usr_login(usr : int, mdp : str, server : str) :
    if not mt5.initialize() : 
         print("MetaTrader5 n'a pas pu être initialisée")
         quit()
    else : 
        if not mt5.login(usr,mdp,server) : 
            print("Vérifiez vos identifiants")
        else : 
            print("Connexion réussie !")

usr_login(usr = 41552251, mdp = "ee4rli8A1iLU", server = "AdmiralMarkets-Demo" )

print(mt5.last_error())

bot1 = bot.TroisMA(mt5symbol="BTCUSD",volume = 0.05,ysymbol="BTC-USD")
print(bot1.mt5symbol)
bot.TroisMA.process_open_buy(bot1)










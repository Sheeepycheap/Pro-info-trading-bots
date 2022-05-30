from Indicateurs import money_to_volume
import bot
import MetaTrader5 as mt5
from tkinter import *
from tkinter import ttk 
from functools import partial
import Indicateurs as ind
from tkinter import messagebox


class Myapp : 
    def __init__(self):
        self.root = Tk()
        self.root.title("PRO 3600")
        self.root.minsize(480,380)
        self.root.geometry("1080x690")
        self.root.config(background="#4A4A4A")
        self.menu_bar()   #Création d'une barre de menu 
        # Initialisation des frames de l'onglet de connexion (début du programme)     
        self.frame_welcome = Frame(self.root, background="#4A4A4A")
        self.connexion_frame()
        self.frame_welcome.pack(expand = YES) 
        # initialisation des frames de l'onglet "bots"
        self.bot_frame = Frame(self.root,bg="#4A4A4A")
        self.accceuil_frame = Frame(self.root,bg="#4A4A4A")
        self.help_frame = Frame(self.root,bg="#4A4A4A")
        # Initialisation des threads à terminer :
        self.pill2kill = []
        # Initialisation des bots qui seront activés
        self.bot_actif = []

    def menu_bar(self) :
        #""
        # Cette méthode permet d'ajouter une barre de menu/navigation. Pour l'instant, le seul menu fonctionnel est 
        # le menu bot
        #""
        nav_bar = Menu(self.root)
        nav_bar.add_command(label = "Acceuil", command = self.to_acceuil)
        file_menu = Menu(nav_bar,tearoff = 0)
        file_menu.add_command(label="Trois Ema", command = self.openWindowStrategyA)
        file_menu.add_command(label = "Zscore", command = self.openWindowStrategyB)
        file_menu.add_command(label = "Eveningstar", command = self.openWindowStrategyC)
        file_menu.add_command(label = "Morningstar", command = self.openWindowStrategyD)
        file_menu.add_command(label = "SAR + MACD + 200 Ema", command = self.openWindowStrategyE)
        nav_bar.add_cascade(label = "Stratégies", menu = file_menu)
        nav_bar.add_command(label = "Bots", command = self.to_bots)        
        nav_bar.add_command(label = "Help", command = self.to_help)     
        self.root.config(menu = nav_bar)

    def hide_frames(self) :
        #""
        #Cette méthode permet de cacher les frames. Elle permet la navigation par la barre de navigation
        #""
        self.frame_welcome.pack_forget()
        self.bot_frame.pack_forget()
        self.bot_frame.destroy()
        self.accceuil_frame.pack_forget()
        self.accceuil_frame.destroy()
        self.help_frame.pack_forget()
        self.help_frame.destroy()

    def to_acceuil(self) :
        self.hide_frames()
        self.acceuil_frame()

    def to_bots(self) : 
        self.hide_frames()
        self.bots_frame() 
    
    def to_help(self) : 
        self.hide_frames()
        self.help_frames()

    def acceuil_frame(self) :
        # ""
        # Cette méthode construit la frame d'acceuil du logiciel
        # Elle contient un tableau référençant les bots activés 
        # "" 
        self.accceuil_frame = Frame(self.root,bg="#4A4A4A")
        tree = ttk.Treeview(self.root, columns = (1,2,3) , height=5, show = "headings")
        tree.place(x = 220 , y = 220 , width = 600 , height = 200)
        tree.heading(1, text="Strategie")
        tree.heading(2, text="Actif")
        tree.heading(3, text="Volume")
        for i in self.bot_actif:
            tree.insert(parent='', index='end', values=(i[0], i[1], i[2]))

    def connexion_frame(self) :
        #""
        # Cette méthode construit le menu de connexion (qui apparaît dès le lancement)
        #""

        #Création des objets (bouton et les commandes, titre...)
        label_title = Label(self.frame_welcome, text="Bienvenue sur l'application !", font =("Courrier",30),bg= "#4A4A4A",fg='white')
        label_subtitle = Label(self.frame_welcome, text="Veuillez indiquer vos identifiants de Connexion MetaTrader5 :", font=("Courrier", 15), bg = "#4A4A4A", fg = 'white')
        label_usr = Label(self.frame_welcome,text="Nom D'utilisateur :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        usernameEntry = Entry(self.frame_welcome,width= 50)
        label_mdp = Label(self.frame_welcome,text="Mot de passe :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        mdpEntry = Entry(self.frame_welcome,width= 50)
        label_server =  Label(self.frame_welcome,text="Serveur :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        servEntry = Entry(self.frame_welcome,width= 50)
        loginButton = Button(self.frame_welcome,text = "Connexion",command = partial(self.usr_login, usernameEntry, mdpEntry,servEntry)) 
        # partial est une fonction permettant le lancement d'une méthode (self.usr_login) uniquement lorsque le boutton est actionné. 
        # Sans partial la méthode usr_login se lance dès l'instanciation, ce qui mène à une erreur. 

        # Empaquetage des objets (bouton,titre...), ce qui permet l'affichage de ces objets. 
        label_title.pack()
        label_subtitle.pack(pady=35)
        label_usr.pack(pady=3)
        usernameEntry.pack(pady=3)
        label_mdp.pack(pady=3)
        mdpEntry.pack(pady=3)
        label_server.pack(pady=3)
        servEntry.pack(pady=3)
        loginButton.pack(pady=3)
    
    
    def usr_login(self,usr , mdp, server ) :
        #""
        # Cette méthode permet la connexion au serveur de MetaTrader5 avec un utilisateur, un mot de passe et un serveur. 
        #""
        if not mt5.initialize() : 
            print("MetaTrader5 n'a pas pu être initialisée")
            quit()
        else :
            a= int(usr.get())
            b = mdp.get()
            c = server.get()
            if not mt5.login(a,b,c) : 
                #messagebox.showerror("Identifiants incorrects","Vérifiez vos identifiants.") 
                print("erreur")
            else : 
                print("Connexion réussie !")
                self.hide_frames()
                self.bots_frame()

    def bots_frame(self) :        
        # Création du texte et des boutons
        self.bot_frame = Frame(self.root,bg="#4A4A4A")
        label_title1 = Label(self.bot_frame,text="Veuillez choisir une ou plusieurs stratégies. \n Pour obtenir plus d'informations sur les stratégies mis en place, allez dans l'onglet Stratégies ", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_strat = Label(self.bot_frame,text="Stratégie :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        liste_strat= ["Choisir une stratégie", "Trois Ema", "Zscore", "Morningstar","Eveningstar","SAR + MACD + 200 Ema"]
        stratEntry = ttk.Combobox(self.bot_frame, value=liste_strat)
        label_vol = Label(self.bot_frame,text="Montant :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        volEntry = Entry(self.bot_frame,width= 25)
        label_actif = Label(self.bot_frame,text="Actif (clé Metatrader) :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        actifEntry = Entry(self.bot_frame,width= 25) 
        label_yfinance = Label(self.bot_frame,text="Actif (clé yfinance) :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        actifEntry_yfinance = Entry(self.bot_frame,width= 25) 
        runButton = Button(self.bot_frame,text = "RUN",bg="#54B22E",fg ='white', command = partial(self.run_strat,stratEntry,volEntry,actifEntry,actifEntry_yfinance)) 
        label_title2 = Label(self.bot_frame,text="Veuillez choisir un bot actif que vous voulez arrêter (STOP ALL termine tous les bots) :", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_tokill = Label(self.bot_frame, text="Indiquez la stratégie que vous voulez arrêtez",font=("Courrier", 10), bg = "#252424", fg = 'white')
        tokillEntry = Entry(self.bot_frame,width= 25)
        kill_allButton = Button(self.bot_frame,text = "KILL ALL",bg="#DB1E00",fg ='white',command = self.kill_all)
        killButton = Button(self.bot_frame,text = "KILL",bg="#DB1E00",fg ='white',width=6, command = partial(self.kill, tokillEntry))
        # Affichage de la frame (empaquettage)
        label_title1.pack(side = TOP)
        label_strat.pack(pady=3)
        stratEntry.pack(pady=5)
        label_vol.pack(pady=3)
        volEntry.pack(pady=3) 
        label_actif.pack(pady=3)
        actifEntry.pack(pady=3)
        label_yfinance.pack(pady=3)
        actifEntry_yfinance.pack(pady=3)
        runButton.pack()
        label_title2.pack()
        label_tokill.pack()
        tokillEntry.pack()
        killButton.pack()
        kill_allButton.pack()
        self.bot_frame.pack(expand = YES)

    def run_strat(self, strat:str , volume : float, mt5_key : str,yfinance_key :str) :
        #""
        # Cette méthode permet de lancer les stratégies en instanciant des objets des classes du fichier bot.py. 
        # Pour l'instant il n'y a qu'une seule stratégie. 
        #""
        if strat.get() == "Trois Ema" : 
            print("Stratégie Trois Ema initialisée ! ")
            Bot = bot.TroisMA(mt5symbol=mt5_key.get(), volume = ind.money_to_volume(mt5_key.get(),float(volume.get())) , ysymbol=yfinance_key.get())
            bot.Bot.open_buy(Bot)
            self.pill2kill.append(Bot)
            self.bot_actif.append(["Trois Ema", Bot.mt5symbol , Bot.volume])
        if strat.get() == "Zscore" : 
            print("Stratégie Zscore initialisée ! ")
            Bot = bot.Zscore(mt5symbol=mt5_key.get(), volume = ind.money_to_volume(mt5_key.get(),float(volume.get())) , ysymbol=yfinance_key.get())
            bot.Bot.open_buy(Bot)
            self.pill2kill.append(Bot)
            self.bot_actif.append(["Zscore", Bot.mt5symbol , Bot.volume]) 
        if strat.get() == "Eveningstar" : 
            print("Stratégie Eveningstar initialisée ! ")
            Bot = bot.reco_eveningstar(mt5symbol=mt5_key.get(), volume = ind.money_to_volume(mt5_key.get(),float(volume.get())) , ysymbol=yfinance_key.get())
            bot.Bot.open_buy(Bot)
            self.pill2kill.append(Bot)
            self.bot_actif.append(["Eveningstar", Bot.mt5symbol , Bot.volume])
        if strat.get() == "Morningstar" : 
            print("Stratégie Morningstar initialisée ! ")
            Bot = bot.reco_morningstar(mt5symbol=mt5_key.get(), volume = ind.money_to_volume(mt5_key.get(),float(volume.get())) , ysymbol=yfinance_key.get())
            bot.Bot.open_buy(Bot)
            self.pill2kill.append(Bot)
            self.bot_actif.append(["Morningstar", Bot.mt5symbol , Bot.volume])
        if strat.get() == "SAR + MACD + 200 Ema" : 
            print("Stratégie PSAR_MACD initialisée ! ")
            Bot = bot.PSAR_MACD(mt5symbol=mt5_key.get(), volume = ind.money_to_volume(mt5_key.get(),float(volume.get())) , ysymbol=yfinance_key.get())
            bot.Bot.open_buy(Bot)
            self.pill2kill.append(Bot)
            self.bot_actif.append(["SAR + MACD + 200 Ema", Bot.mt5symbol , Bot.volume])

    def kill(self,tokillEntry) : 
        num = int(tokillEntry.get())
        bot.Bot.kill(self.pill2kill[num])
        self.pill2kill.pop(num)
        self.bot_actif.pop(num)
        print(self.pill2kill)
        print(self.bot_actif)
    
    def kill_all(self) : 
        # ""
        # Cette méthode permet de terminer tous les bots en faisant appel à la méthode kill() de leurs classes.
        # ""
        for thread in self.pill2kill :
            bot.Bot.kill(thread) 

        for j in range(len(self.pill2kill)) :
            self.pill2kill.pop(0)
            self.bot_actif.pop(0)
            
        print(self.pill2kill)
        print(self.bot_actif)

    def help_frames(self):
        # ""
        # Cette fonction permet d'afficher la frame d'aide contenant les instructions pour se servir du logiciel
        # ""
        self.help_frame = Frame(self.root,bg="#4A4A4A")
        help_title= Label(self.help_frame,text="Tutoriel pour se servir de ce logiciel de trading", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        help_title.pack(expand=YES)
        help_txt= Label(self.help_frame, text="Votre compte MetaTrader5 est directement connecté à ce logiciel, \n pour démarrer votre session il vous suffit de vous rendre dans la section bot pour en créer un nouveau. \n Vous devrez choisir une stratégie (toutes les informations relatives à chacun sont condensées dans l'onglet stratégie), \n un volume à trader ainsi que votre actif d'intérêt. Une fois lancé, toutes les informations relatives\n à votre bot se retrouveront sur la frame principale", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        help_txt.pack(expand=YES) #les informations liées seront ainsi ajoutées à la page
        self.help_frame.pack(expand=YES)
    # Les 5 fonctions openWindowStrategy servent à ouvrir des pages contenant l'ensemble des informations relatives à chacune des stratégies implémentées
    # Leur construction est identique, seul le fichier texte diffère
    def openWindowStrategyA(self):
        newWindowA= Toplevel(self.root)
        newWindowA.title("Stratégie Trois Ema")
        newWindowA.geometry("1080x720")
        newWindowA.config(background="#4A4A4A")
        newWindowA.minsize(720,480)
        strat_A= Label(newWindowA,text="Comment fonctionne la stratégie ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_A1= Label(newWindowA, text="Lorsque les trois ema ( 5 20 60) sont croisées positivement \n alors on a un signal d'achat. Si elles sont croisées négativement on a un signal de sell", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_A.pack(expand=YES)
        strat_A1.pack(expand = YES)
    
    def openWindowStrategyB(self):
        newWindowB= Toplevel(self.root)
        newWindowB.title("Stratégie Zscore")
        newWindowB.geometry("1080x720")
        newWindowB.config(background="#4A4A4A")
        newWindowB.minsize(720,480)
        strat_B= Label(newWindowB,text="Comment fonctionne la stratégie ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_B1= Label(newWindowB, text="Lorsque le zscore est supérieur 2.4 alors on a un signal short, on fait exclusivement des shorts", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_B.pack(expand=YES)
        strat_B1.pack(expand = YES)

    def openWindowStrategyC(self):
        newWindowC= Toplevel(self.root)
        newWindowC.title("Stratégie Eveningstar")
        newWindowC.geometry("1080x720")
        newWindowC.config(background="#4A4A4A")
        newWindowC.minsize(720,480)
        strat_C= Label(newWindowC,text="Comment fonctionne la stratégie ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_C1 = Label(newWindowC, text = "Lorsque la bougie est un marteau (c'est à dire longue meche vers le bas \n et petit corp mais la fermeture est supérieure à l'ouverture) après des bougies rouges alors on a des bons signaux buy", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_C.pack(expand=YES)
        strat_C1.pack(expand = YES)
    
    def openWindowStrategyD(self):
        newWindowC= Toplevel(self.root)
        newWindowC.title("Stratégie Morningstar")
        newWindowC.geometry("1080x720")
        newWindowC.config(background="#4A4A4A")
        newWindowC.minsize(720,480)
        strat_D= Label(newWindowC,text="Comment fonctionne la stratégie ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_D1 = Label(newWindowC, text = "Lorsque la bougie est un une étoile du matin (c'est à dire longue meche au dessus \n de la bougie et petit corp mais la fermeture est inférieure à l'ouverture) après des bougies vertes alors on a \n des bons signaux short", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_D.pack(expand=YES)
        strat_D1.pack(expand = YES)
    
    def openWindowStrategyE(self):
        newWindowC= Toplevel(self.root)
        newWindowC.title("Stratégie SAR + MACD + 200 Ema")
        newWindowC.geometry("1080x720")
        newWindowC.config(background="#4A4A4A")
        newWindowC.minsize(720,480)
        strat_E= Label(newWindowC,text="Comment fonctionne la stratégie ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_E1 = Label(newWindowC, text ="Lorsque le MACD est postif et que le prix est audessus de l'EMA 200 \n alors on prend tout les signaux buy issus du SAR (SAR = bull). Lorsque le MACD est négatif et que le prix en dessous de l'EMA 200 \n alors on prend tout les signaux sell du SAR ( SAR = bear) ", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_E.pack(expand=YES)
        strat_E1.pack(expand = YES)


test = Myapp()
test.root.mainloop()
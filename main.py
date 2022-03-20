from Indicateurs import money_to_volume
import bot
import MetaTrader5 as mt5
from tkinter import *
from functools import partial
import Indicateurs as ind


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
        # Initialisation des threads à terminer :
        self.pill2kill = []


    def menu_bar(self) :
        #""
        # Cette méthode permet d'ajouter une barre de menu/navigation. Pour l'instant, le seul menu fonctionnel est 
        # le menu bot
        #""
        nav_bar = Menu(self.root)
        nav_bar.add_command(label = "Acceuil")
        file_menu = Menu(nav_bar,tearoff = 0)
        file_menu.add_command(label="Stratégie A")
        file_menu.add_command(label = "Stratégie B")
        file_menu.add_command(label = "Bref t'as compris ...")
        nav_bar.add_cascade(label = "Stratégies", menu = file_menu)
        nav_bar.add_command(label = "Bots")        
        nav_bar.add_command(label = "Help")    
        nav_bar.add_command(label = "Déconnexion")  
        self.root.config(menu = nav_bar)
     
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
    
    def hide_frames(self) :
        #""
        # Cette méthode permet de cacher les frames. Elle permet la navigation par la barre de navigation
        #""
        self.frame_welcome.pack_forget()
        self.bot_frame.pack_forget()
    
    def usr_login(self,usr , mdp, server ) :
        #""
        # Cette méthode permet la connexion au serveur de MetaTrader5 avec un utilisateur, un mot de passe et un serveur. 
        #""
        if not mt5.initialize() : 
            print("MetaTrader5 n'a pas pu être initialisée")
            quit()
        else : 
            if not mt5.login(int(usr.get()),mdp.get(),server.get()) : 
                print("Vérifiez vos identifiants")
            else : 
                print("Connexion réussie !")
                self.hide_frames()
                self.bots_frame()

    def bots_frame(self) :        
        # Création du texte et des boutons
        label_title1 = Label(self.bot_frame,text="Veuillez choisir une ou plusieurs stratégies. \n Pour obtenir plus d'informations sur les stratégies mis en place, allez dans l'onglet Stratégies ", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_strat = Label(self.bot_frame,text="Stratégie :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        stratEntry = Entry(self.bot_frame,width= 25)
        label_vol = Label(self.bot_frame,text="Montant :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        volEntry = Entry(self.bot_frame,width= 25)
        label_actif = Label(self.bot_frame,text="L'actif :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        actifEntry = Entry(self.bot_frame,width= 25) 
        runButton = Button(self.bot_frame,text = "RUN",bg="#54B22E",fg ='white', command = partial(self.run_strat,stratEntry,volEntry,actifEntry)) 
        label_title2 = Label(self.bot_frame,text="Veuillez choisir un bot actif que vous voulez arrêter (STOP ALL termine tous les bots) :", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_tokill = Label(self.bot_frame, text="Indiquez la stratégie que vous voulez arrêtez",font=("Courrier", 10), bg = "#252424", fg = 'white')
        tokillEntry = Entry(self.bot_frame,width= 25)
        kill_allButton = Button(self.bot_frame,text = "KILL ALL",bg="#DB1E00",fg ='white',command = self.kill_all)
        killButton = Button(self.bot_frame,text = "KILL",bg="#DB1E00",fg ='white',width=6)
        # Affichage de la frame (empaquettage)
        label_title1.pack(side = TOP)
        label_strat.pack(pady=3)
        stratEntry.pack(pady=3)
        label_vol.pack(pady=3)
        volEntry.pack(pady=3) 
        label_actif.pack(pady=3)
        actifEntry.pack(pady=3)
        runButton.pack()
        label_title2.pack()
        label_tokill.pack()
        tokillEntry.pack()
        killButton.pack()
        kill_allButton.pack()
        self.bot_frame.pack(expand = YES)

    def run_strat(self, strat:str , volume : float, market : str) :
        #""
        # Cette méthode permet de lancer les stratégies en instanciant des objets des classes du fichier bot.py. 
        # Pour l'instant il n'y a qu'une seule stratégie. 
        #""
        if strat.get() == "Trois Ema" : 
            print("ok")
            Bot = bot.TroisMA(mt5symbol=market.get(), volume = ind.money_to_volume(market.get(),float(volume.get())) , ysymbol="BTC-USD")
            Bot.open_buy()
            self.pill2kill.append(Bot)
    
    def kill_all(self) : 
        # ""
        # Cette méthode permet de terminer tous les bots en faisant appel à la méthode kill() de leurs classes.
        # ""
        print(self.pill2kill)
        for thread in self.pill2kill :
            if isinstance(thread,bot.TroisMA) :
                print("ok")
                bot.TroisMA.kill(thread)


test = Myapp()
test.root.mainloop()



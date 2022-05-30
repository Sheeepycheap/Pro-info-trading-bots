from tkinter import *
from tkinter import ttk
from functools import partial


class Myapp :
    def __init__(self):
        self.root = Tk()
        self.root.title("TEST")
        self.root.minsize(480,380)
        self.root.geometry("1080x720")
        self.root.config(background="#4A4A4A")
        self.gestion_bot_frame = Frame(self.root, bg="#4A4A4A")
        self.menu_bar()
        self.pill2kill = []

    def hide_frame_bot(self) :
        #""
        # Cette méthode permet de cacher les frames. Elle permet la navigation par la barre de navigation
        #""
        self.bot_frame.pack_forget()

    def menu_bar(self):
        nav_bar = Menu(self.root)
        nav_bar.add_command(label = "Acceuil")
        file_menu = Menu(nav_bar,tearoff = 0)
        file_menu.add_command(label="Stratégie A", command= self.openWindowStrategyA)
        file_menu.add_command(label = "Stratégie B", command= self.openWindowStrategyB)
        file_menu.add_command(label = "Stratégie C", command= self.openWindowStrategyC)
        nav_bar.add_cascade(label = "Stratégies", menu = file_menu)
        menu_bot = Menu(nav_bar, tearoff = 0)
        menu_bot.add_command(label = "Créer un nouveau bot", command = self.bots_window)
        menu_bot.add_command(label = "Gestion des bots", command = self.gestion_bots_frame) 
        nav_bar.add_cascade(label = "Bots", menu= menu_bot)      
        menu_help = Menu(nav_bar, tearoff = 0) 
        menu_help.add_command(label = "Comment se servir du logiciel ?", command = self.openWindowHelp)
        nav_bar.add_cascade(label = "Help", menu = menu_help)  
        nav_bar.add_command(label = "Déconnexion")  
        self.root.config(menu = nav_bar)

    def bots_window(self) :        
        botWindow= Toplevel(self.root)
        botWindow.title("Création d'un nouveau bot")
        botWindow.geometry("720x360")
        botWindow.config(background="#4A4A4A") 
        botWindow.minsize(720,360)
        label_title1 = Label(botWindow,text="Veuillez choisir une ou plusieurs stratégies. \n Pour obtenir plus d'informations sur les stratégies mis en place, allez dans l'onglet Stratégies ", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_strat = Label(botWindow,text="Stratégie", font=("Courrier", 10), bg = "#252424", fg = 'white')
        liste_strat= ["Choisir une stratégie", "Stratégie A", "Stratégie B", "Stratégie C"]
        listeCombo = ttk.Combobox(botWindow, value=liste_strat)
        listeCombo.current(0)
        label_vol = Label(botWindow,text="Montant", font=("Courrier", 10), bg = "#252424", fg = 'white')
        volEntry = Entry(botWindow,width= 25)
        label_actif = Label(botWindow,text="L'actif", font=("Courrier", 10), bg = "#252424", fg = 'white')
        liste_actif= ["Choisir un actif", "BTC-EUR", "ETH-EUR"]
        listeCombo2 = ttk.Combobox(botWindow, value=liste_actif)
        listeCombo2.current(0)
        label_actif_yf = Label(botWindow,text="Actif Yahoo Finance", font=("Courier", 10), bg = "#252424", fg = 'white')
        volActifyf = Entry(botWindow,width= 25)
        runButton = Button(botWindow,text = "RUN") 

        # Affichage de la frame (empaquettage)
        label_title1.pack(side = TOP)
        label_strat.pack(pady=5)
        listeCombo.pack(pady=5)
        label_vol.pack(pady=5)
        volEntry.pack(pady=5) 
        label_actif.pack(pady=5)
        listeCombo2.pack(pady=5)
        label_actif_yf.pack(pady=5)
        volActifyf.pack(pady=5)
        runButton.pack(pady=10)


    def gestion_bots_frame(self): 
        tree = ttk.Treeview(self.gestion_bot_frame, columns = (1,2,3) , height=5, show = "headings")
        tree.place(x = 0 , y = 0 , width = 600 , height = 200)
        tree.heading(1, text="Numéro")
        tree.heading(2, text="Bots activés")
        tree.heading(3, text="Actif")
        label_title2 = Label(self.gestion_bot_frame,text="Veuillez choisir un bot actif que vous voulez arrêter (STOP ALL termine tous les bots) :", font =("Courrier",15),bg= "#4A4A4A",fg='white' )
        label_tokill = Label(self.gestion_bot_frame, text="Indiquez le numéro du bot à arrêter",font=("Courrier", 10), bg = "#252424", fg = 'white')
        num_bot = Entry(self.gestion_bot_frame,width= 25)
        kill_allButton = Button(self.gestion_bot_frame,text = "KILL ALL")
        killButton = Button(self.gestion_bot_frame,text = "KILL")
        label_title2.pack(pady=10)
        label_tokill.pack(pady=5)
        num_bot.pack(pady=5)
        killButton.pack(pady=5)
        kill_allButton.pack(pady=5)
        
        self.gestion_bot_frame.pack(expand = YES)




    #On aborde ici des fonctions qui vont permettre le fonctionnement de la barre de menu du front : par nature ces fonctions n'ont
    #aucun lien avec le back, elles ne servent qu'à afficher une nouvelle page avec à l'intérieur un fichier texte soit pour expliquer
    #le fonctionnement du bot, soit pour obtenir des informations sur chaque stratégie implémentée. Le choix d'ouvrir une nouvelle page
    #plutôt que de changer de frame est purement ergonomique. En effet si l'on veut comparer 2 stratégies, ou utiliser le bot tout en lisant
    #les instructions, il apparaissait plus logique d'ouvrir à chaque fois une nouvelle page.

    def openWindowHelp(self):
        #Fonction qui va nous permettre d'ouvrir une page avec les différentes instructions pour se servir de notre logiciel
        newWindow= Toplevel(self.root) #création d'une nouvelle page par dessus celle désignée root
        newWindow.title("Menu d'aide")
        newWindow.geometry("1080x720")
        newWindow.config(background="#4A4A4A") #configuration de la nouvelle page
        newWindow.minsize(720,480)
        help_title= Label(newWindow,text="Tutoriel pour se servir de ce logiciel de trading", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        help_title.pack(expand=YES)
        help_txt= Label(newWindow, text="Votre compte MetaTrader5 est directement connecté à ce logiciel, \n pour démarrer votre session il vous suffit de vous rendre dans la section bot pour en créer un nouveau. \n Vous devrez choisir une stratégie (toutes les informations relatives à chacun sont condensées dans l'onglet stratégie), \n un volume à trader ainsi que votre actif d'intérêt. Une fois lancé, toutes les informations relatives\n à votre bot se retrouveront sur la frame principale", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        help_txt.pack(expand=YES) #les informations liées seront ainsi ajoutées à la page

    #les stratégies suivantes permettent d'afficher les informations liées aux stratégies. Elles sont assez répétitives mais il apparaissait
    #plus simple pour la compréhension du code de faire plusieurs fois la même fonction similaire plutôt qu'une seule fonction

    def openWindowStrategyA(self):
        newWindowA= Toplevel(self.root)
        newWindowA.title("Stratégie A")
        newWindowA.geometry("1080x720")
        newWindowA.config(background="#4A4A4A")
        newWindowA.minsize(720,480)
        strat_A= Label(newWindowA,text="Comment fonctionne la stratégie A ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_A.pack(expand=YES)
    
    def openWindowStrategyB(self):
        newWindowB= Toplevel(self.root)
        newWindowB.title("Stratégie B")
        newWindowB.geometry("1080x720")
        newWindowB.config(background="#4A4A4A")
        newWindowB.minsize(720,480)
        strat_A= Label(newWindowB,text="Comment fonctionne la stratégie B ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_A.pack(expand=YES)

    def openWindowStrategyC(self):
        newWindowC= Toplevel(self.root)
        newWindowC.title("Stratégie C")
        newWindowC.geometry("1080x720")
        newWindowC.config(background="#4A4A4A")
        newWindowC.minsize(720,480)
        strat_A= Label(newWindowC,text="Comment fonctionne la stratégie C ?", font =("Courrier",15),bg= "#4A4A4A",fg='white')
        strat_A.pack(expand=YES)

test = Myapp()
test.root.mainloop()
from tkinter import *
import MetaTrader5 as mt5
from functools import partial


class Myapp : 
    def __init__(self):
        self.root = Tk()
        self.root.title("PRO 3600")
        self.root.minsize(480,380)
        self.root.geometry("1080x690")
        self.root.config(background="#4A4A4A")
        #Création d'une barre de menu 
        self.menu_bar()   
        # Initialisation des frames de l'onglet de connexion (début du programme)     
        self.frame_welcome = Frame(self.root, background="#4A4A4A")
        self.connexion_frame()
        self.frame_welcome.pack(expand = YES) 
        # initialisation des frames de l'onglet "bots"
        self.bots_frame_1 = Frame(self.root,bg="#4A4A4A")
        self.bots_frame_2 = Frame(self.root,bg="#4A4A4A")
        self.bots_frame_3 = Frame(self.root,bg="#4A4A4A")
        self.bots_frame_4 = Frame(self.root,bg="#4A4A4A")


    def menu_bar(self) :
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
        label_title = Label(self.frame_welcome, text="Bienvenue sur l'application !", font =("Courrier",30),bg= "#4A4A4A",fg='white')
        label_subtitle = Label(self.frame_welcome, text="Veuillez indiquer vos identifiants de Connexion MetaTrader5 :", font=("Courrier", 15), bg = "#4A4A4A", fg = 'white')
        label_usr = Label(self.frame_welcome,text="Nom D'utilisateur :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        usernameEntry = Entry(self.frame_welcome,width= 50)
        label_mdp = Label(self.frame_welcome,text="Mot de passe :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        mdpEntry = Entry(self.frame_welcome,width= 50)
        label_server =  Label(self.frame_welcome,text="Serveur :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        servEntry = Entry(self.frame_welcome,width= 50)

        loginButton = Button(self.frame_welcome,text = "Connexion",command = partial(self.usr_login, usernameEntry, mdpEntry,servEntry))


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
        self.frame_welcome.pack_forget()
    
    def usr_login(self,usr , mdp, server ) :
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
        label_title1 = Label(self.bots_frame_1,text="Veuillez choisir une ou plusieurs stratégies. \n Pour obtenir plus d'informations sur les stratégies mis en place, allez dans l'onglet Stratégies ", font =("Courrier",15),bg= "#4A4A4A",fg='white' )

        
        label_strat = Label(self.bots_frame_1,text="Stratégie :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        stratEntry = Entry(self.bots_frame_1,width= 25)
        label_vol = Label(self.bots_frame_1,text="Montant :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        volEntry = Entry(self.bots_frame_1,width= 25)
        label_actif = Label(self.bots_frame_1,text="L'actif :", font=("Courrier", 10), bg = "#252424", fg = 'white')
        actifEntry = Entry(self.bots_frame_1,width= 25) 
        runButton = Button(self.bots_frame_1,text = "RUN",bg="#54B22E",fg ='white') 
        
        label_title2 = Label(self.bots_frame_2,text="Veuillez choisir un bot actif que vous voulez arrêter (STOP ALL termine tous les bots) :", font =("Courrier",15),bg= "#4A4A4A",fg='white' )

        label_title1.pack(side = TOP)
        label_strat.pack(pady=3)
        stratEntry.pack(pady=3)
        label_vol.pack(pady=3)
        volEntry.pack(pady=3)
        label_actif.pack(pady=3)
        actifEntry.pack(pady=3)
        runButton.pack()
        label_title2.pack()
        self.bots_frame_1.pack(expand=YES)
        self.bots_frame_2.pack(expand=YES)












test = Myapp()
test.root.mainloop()

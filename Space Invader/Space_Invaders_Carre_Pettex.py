# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:45:02 2021

@author: Amaury Carré et Matthieu Pettex

état du projet = fini
"""
from tkinter import Tk, Button, Canvas, PhotoImage, Label, messagebox
from random import randint

Partie_en_cours=False
TirsAlien=[] #gère le nombre de tirs aliens présents dans la partie
TirsBoss=[]  #gère le nombre de tirs du boss présents dans la partie
#fenetre--------------------------------------------------
largeur=1350 #gère les dimensions de la fenetre de jeu
hauteur=700

#Joueur---------------------------------------------------
VitesseTir=5 #gère la vitesse à laquelle le laser se déplace sur la fenetre
Tirs=[] #gère le nombre de tirs du joueur présents dans la partie
largeur_vaisseau=101 #gère la hitbos horizontale du joueur
VitesseDeplacement=10 #gère le nombre de pixel parcouru par le joueur en une pression de touche 
TempsEntreTirs=1 #gère le temps minimal écoulé entre deux tirs


#mechant-------------------------------------------------
#idem que le joueur
largeur_alien=50
hauteur_alien=50
ecart_alien=25 #écart entre deux aliens sur une ligne lors de leur création
hauteur_alien_ligne1=50
nbre_alien_par_ligne=15 #nombre d'aliens créés par ligne
descente_alien=20 #gère le nombre de pixel que les aliens descendent lorsqu'il finissent de se déplacer sur une ligne
VitesseDeplacement=20 #gère le nombre de pixel parcouru par l'alien toutes les 20 millisecondes
VitesseAlien=3 
AccelerationAlien=0.25 #rajoute 0.25 de vitesse de déplacement à chaque fois qu'un alien est éliminé
tps_entre_tir_alien=1000 #un tir est déclenché par TOUS les aliens toutes les secondes
#boss-----------------------------------------------------
#idem que le joueur
largeur_boss=75
hauteur_boss=113
ecart_boss=100 #inutile car il n'y a qu'un boss mais on y laisse si on souhaite apporter plus tard des améliorations au jeu
hauteur_boss_ligne1=50
nbre_boss_par_ligne=1
descente_boss=100 #gère le nombre de pixel que le boss descend lorsqu'il finit de se déplacer sur une ligne
VitesseDeplacement=20
VitesseBoss=3
tps_entre_tir_boss=1000 #un tir est déclenché par le boss toutes les secondes
vieBoss=5 #cette variable va être mise à jour lorsque le boss se fera toucher par les lasers du joueur
vieBossI=5 #cette variable ne change pas de valeur au cours de la partie



#la class Joueur initialise le joueur, son déplacement ainsi que l'état 
#dans lequel il est (vivant ou mort).
class Joueur():
    global Vies
    def __init__(self): #création des variables de la classe
       self.vivant=True
       self.x=x1
       self.y=y1
       self.apparence=canevas.create_image(self.x,self.y,anchor='center',image=playerImg)

    def deplacement(self,dir):#gère le déplacement du joueur et vérifie que le joueur ne sorte pas de la zone de jeu
       if self.x >= largeur_vaisseau/2 and dir==-1:
           self.x += VitesseDeplacement*dir
       elif self.x <= largeur-largeur_vaisseau/2 and dir==1:
           self.x += VitesseDeplacement*dir
       self.Affichage()
       
    def Affichage(self):#affiche le joueur et le fait disparaitre s'il n'a plus de vie
        if Vies<0.5:
            canevas.delete(self.apparence)
            self.vivant=False
            messagebox.showinfo("Partie Finie", "Vous avez perdu !")
            fenetre.quit()
            
        else:
            canevas.coords(self.apparence,self.x,self.y)
   
#la class Tir s'occupe des tirs du Joueur: mouvement et disparition        
class Tir():
    Compteur=0
    def __init__(self):#création des variables de la classe
        self.x=vaisseau.x
        self.y=vaisseau.y
        self.apparence=canevas.create_image(self.x , self.y ,image=laserImgJoueur)
        self.encours=True
        Tir.Compteur+=1
    
    def Affichage(self):#affiche le tir
        canevas.coords(self.apparence , self.x , self.y-10)
    
    def Deplacement(self):#gère le déplacement du laser du joueur
        if self.encours:
            self.y-=VitesseTir
            self.Affichage()
            self.FinTir()
            fenetre.after(5,self.Deplacement)
            
    def FinTir(self):#si le tir sort de la zone de jeu ou s'il touche un ennemie, il disparait
        global encours, vieBoss
        if self.y<0:
            self.encours=False
            canevas.delete(self.apparence)
            del Tirs[0]
            Tir.Compteur-=1            
        else:
            for i in ennemie:
                if i.vivant and self.y>=i.y and self.y<=i.y+hauteur_alien and self.x<=i.x+largeur_alien and self.x>=i.x:
                    self.Destruction()
                    canevas.delete(i.apparence)
                    i.vivant=False
                    mechant.vitesse+=AccelerationAlien
                    PartieGagnee()
            for i in ennemieB:
                if i.vivant and self.y>=i.y and self.y<=i.y+hauteur_boss and self.x<=i.x+largeur_boss and self.x>=i.x:
                    self.Destruction()
                    vieBoss-=1
                    if vieBoss==0:
                        canevas.delete(i.apparence)
                        i.vivant=False
                        PartieGagnee()

    def Destruction(self):    #détruit le tir et donne 10 de score si le tir est détruit en touchant un ennemi
        global Score, ennemieB
        self.encours=False
        canevas.delete(self.apparence)
        del Tirs[0]
        Tir.Compteur-=1 
        Score+=10
        if Score==50: #le boss apparait une fois que 5 ennemies de bases ont été tués
            for i in range(nbre_boss_par_ligne):
                ennemieB.append(boss())
            for i in ennemieB:
                i.CreationB()
            deplacerBoss()
            Tir_Boss()
        scoreLabel.config(text = "Score :"+str(Score))#le score est mis à jour dans la zone de jeu en haut à gauche
        
        

#la class TirBoss s'occupe des Tirs du Boss: déplacement et disparition
class TirBoss:
    global Vies
    def __init__(self,i):#création des variables de la classe
        self.x=ennemieB[i].x
        self.y=ennemieB[i].y
        self.apparence=canevas.create_image(self.x , self.y , image=laserImgBoss)
        self.encours=True
        self.Deplacement()

    def affichage(self):#affiche les bombes du boss
        canevas.coords(self.apparence , self.x , self.y)
        
    def Deplacement(self):#idem que joueur
        if self.encours:
            self.y+=VitesseTir-1.5
            self.affichage()
            self.FinTir()
            canevas.after(5,self.Deplacement)
    
    def FinTir(self):#idem que joueur
        global Vies
        if self.y>hauteur:
            self.encours=False
            canevas.delete(self.apparence)
            del TirsBoss[0]
        elif self.y>=vaisseau.y-5 and self.y<=vaisseau.y+5 and\
            self.x<=vaisseau.x+largeur_vaisseau/2 and\
            self.x>=vaisseau.x-largeur_vaisseau/2 :
                self.encours=False
                canevas.delete(self.apparence)
                del TirsBoss[0]
                Vies-=2
                viesLabel.config(text = "Vies :"+str(Vies))
                vaisseau.Affichage()
        else:
            for i in Defences:
                if i.Resistance>0 and self.x>=i.x and self.x<=i.x+largeur_protections and self.y>=Protections.y and self.y<=Protections.y+hauteur_protections:
                    i.Update()
                    self.encours=False
                    canevas.delete(self.apparence)
                    del TirsBoss[0]
 
#la class TirAlien s'occupe des Tirs des Aliens: déplacement et disparition                   
class TirAlien:
    global Vies
    def __init__(self,i):#création des variables de la classe
        self.x=ennemie[i].x  
        self.y=ennemie[i].y
        self.apparence=canevas.create_image(self.x , self.y , image=laserImgMechant)
        self.encours=True
        self.Deplacement()

    def affichage(self):#idem que joueur
        canevas.coords(self.apparence , self.x , self.y)
        
    def Deplacement(self):#idem que joueur
        if self.encours:
            self.y+=VitesseTir-1.5
            self.affichage()
            self.FinTir()
            canevas.after(5,self.Deplacement)
    
    def FinTir(self):#idem que joueur
        global Vies
        if self.y>hauteur:
            self.encours=False
            canevas.delete(self.apparence)
            del TirsAlien[0]
        elif self.y>=vaisseau.y-5 and self.y<=vaisseau.y+5 and\
            self.x<=vaisseau.x+largeur_vaisseau/2 and\
            self.x>=vaisseau.x-largeur_vaisseau/2 :
                self.encours=False
                canevas.delete(self.apparence)
                del TirsAlien[0]
                Vies-=1
                viesLabel.config(text = "Vies :"+str(Vies))
                vaisseau.Affichage()
        else:
            for i in Defences:
                if i.Resistance>0 and self.x>=i.x and self.x<=i.x+largeur_protections and self.y>=Protections.y and self.y<=Protections.y+hauteur_protections:
                    i.Update()
                    self.encours=False
                    canevas.delete(self.apparence)
                    del TirsAlien[0] 

#crée les protections et gère les vies des protections                   
class Protections:
    Compteur=0
    def __init__(self):#création des variables de la classe
        Protections.Compteur+=1
        self.Compteur=Protections.Compteur
        self.x=largeur*self.Compteur/(nbre_protections+1)
        Protections.y=posY_protections
        self.Resistance=resistance_protections
        self.Apparence=canevas.create_rectangle(self.x,self.y,self.x+largeur_protections,self.y+hauteur_protections,width=2,outline='purple',fill='white')
        self.VieProtection=canevas.create_text(self.x+largeur_protections/2,self.y+hauteur_protections/2,text=str(self.Resistance),fill='red')
        
    def Update(self):#supprime la protection si elle n'a plus de vie
        self.Resistance-=1
        if self.Resistance>0:
            canevas.itemconfig(self.VieProtection,text=(str(self.Resistance)))
        else:
            self.Destruction()
    
    def Destruction(self):#supprime la protection
        canevas.delete(self.Apparence)
        canevas.delete(self.VieProtection)
        
#crée une nouvelle partie, le joueur, les ennemies, les défences     
def NouvellePartie():
    global vaisseau, Partie_en_cours, ennemie, ennemieB, Defences
    vaisseau=Joueur()
    Partie_en_cours=True
    ennemie=[]
    ennemieB=[]
    Protections.Compteur=0
    Defences=[Protections() for i in range(nbre_protections)]
    for i in range(nbre_alien_par_ligne):
        ennemie.append(mechant())
    for i in ennemie:
        i.Creation()
    deplacerMechant()
    Tir_Alien()
 
#la class boss 
class boss():
    Compteur=0
    def __init__(self):#création des variables de la classe
        boss.Compteur += 1
        self.Compteur=boss.Compteur
        self.vivant=True
        self.x=self.Compteur*(ecart_boss+largeur_boss)
        y5 = 57
        boss.y=y5
        boss.dir=1
        boss.vitesse=VitesseBoss

    def CreationB(self):#créé le boss
        self.apparence=canevas.create_image(self.x,self.y,anchor='nw',image=Boss)

    def Affichage(self):#affiche le boss
        canevas.coords(self.apparence,self.x,self.y)
        

def deplacerBoss():
    global boutonPlay, ennemieB
    if Partie_en_cours:
        L=[i.vivant for i in ennemieB]
        if True in L:
            i=L.index(True)
            L.reverse()
            j=L.index(True)
            if (ennemieB[-j-1].x+largeur_boss>=largeur and boss.dir==1) or\
            (ennemieB[i].x-largeur_boss<=0 and boss.dir==-1):
                boss.dir*=-1
                boss.y+=descente_boss
                if boss.y>y1:
                    canevas.delete(playerImg)
                    messagebox.showinfo("Partie Finie", "Vous avez perdu !")
                    fenetre.quit()
            for i in ennemieB:
                i.x+=boss.vitesse*boss.dir
                i.Affichage()
        canevas.after(20,deplacerBoss)
        return
#génère les tirs du boss       
def Tir_Boss():
    global ennemieB,TirsBoss 
    if Partie_en_cours:
        L=[i.vivant for i in ennemieB]
        i=randint(0,len(ennemieB)-1)
        if L[i]:
            TirsBoss.append(TirBoss(i))
            canevas.after(tps_entre_tir_boss,Tir_Boss)
        else:
            canevas.after(3,Tir_Boss)

#génère les tirs des aliens
def Tir_Alien():
    global ennemie, TirsAlien 
    if Partie_en_cours:
        L=[i.vivant for i in ennemie]
        i=randint(0,len(ennemie)-1)
        if L[i]:
            TirsAlien.append(TirAlien(i))
            canevas.after(tps_entre_tir_alien,Tir_Alien)
        else:
            canevas.after(3,Tir_Alien)            

#la class méchant s'occupe des aliens mais pas du boss           
class mechant():
    Compteur=0
    def __init__(self):
        mechant.Compteur += 1
        self.Compteur=mechant.Compteur
        self.vivant=True
        self.x=self.Compteur*(ecart_alien+largeur_alien)
        y0 = 28
        mechant.y=y0
        mechant.dir=1
        mechant.vitesse=VitesseAlien

    def Creation(self):
        self.apparence=canevas.create_image(self.x,self.y,anchor='nw',image=enemyImg)

    def Affichage(self):
        canevas.coords(self.apparence,self.x,self.y)
        
#fonction qui s'occupe des déplacements des ennemies mineurs
def deplacerMechant():
    global boutonPlay, ennemie
    if Partie_en_cours:
        boutonPlay.pack_forget()
        L=[i.vivant for i in ennemie]
        if True in L:
            i=L.index(True)
            L.reverse()
            j=L.index(True)
            if (ennemie[-j-1].x+largeur_alien>=largeur and mechant.dir==1) or\
            (ennemie[i].x-largeur_alien<=0 and mechant.dir==-1):
                mechant.dir*=-1
                mechant.y+=descente_alien
                if mechant.y>y1:
                    canevas.delete(playerImg)
                    messagebox.showinfo("Partie Finie", "Vous avez perdu !")
                    fenetre.destroy()
            for i in ennemie:
                i.x+=mechant.vitesse*mechant.dir
                i.Affichage()
        canevas.after(20,deplacerMechant)
        return

#permet l'utilisation du clavier pour jouer soit avec les flèches, soit avec les touches d et q.    
def Clavier(event):
    global TempsTir, tir
    touche=event.keysym
    if touche=='q' or touche=='Left':
        vaisseau.deplacement(-1)
    if touche=='d' or touche=='Right':
        vaisseau.deplacement(1)
    elif touche=='space':
        if Tirs==[] or len(Tirs)<2:#vérifie que le joueur n'ait pas plus de deux tirs présent dans la zone de jeu
            tir=Tir()
            Tirs.append(tir)
            Tirs[Tir.Compteur-1].Deplacement()

#annonce la victoire du joueur    
def PartieGagnee():
    global Score, ennemie, ennemieB, vieBossI
    if Score== (len(ennemie)*10 + len(ennemieB)*vieBossI*10) : #la partie est gagnée quand tout les ennemis ont été éliminés
            messagebox.showinfo("Partie Finie", "Vous avez gagné !")
            fenetre.quit()
        
        
        
#---------fenetre tkinter--------------------------------
fenetre=Tk()
fenetre.title('Battle For Geonosis | By Matthieu Pettex and Amaury Carre')
fenetre.geometry("1350x700")  

#---------objet------------------------------------------
canevas = Canvas(width=largeur, height=hauteur)
canevas.pack(expand=1, fill="both")

#---------images-----------------------------------------
bgImg = PhotoImage(file="Images/planet2.jpeg")
width2 = bgImg.width()
height2 = bgImg.height()
x2 = (width2)/2
y2 = (height2)/2
bg = canevas.create_image(x2, y2, image=bgImg)

Boss = PhotoImage(file="Images/badguy.png")

enemyImg = PhotoImage(file="Images/vultur.png")
width1 = enemyImg.width()
height1 = enemyImg.height()
x0 = (width1)/2
y0 = (height1)/2

playerImg = PhotoImage(file="Images/joueur.png")
x1,y1=660,600

laserImgJoueur=PhotoImage(file="Images/joueur_ammo.png")
laserImgMechant=PhotoImage(file="Images/vultur_ammo.png")
laserImgBoss=PhotoImage(file="Images/bomber_ammo.png")

#--------touche bind-------------
fenetre.bind("<Key>",Clavier)

#--------bouton------------------
boutonQuit=Button(canevas, text ='Quitter', bg="orange", command=fenetre.quit)#permet de fermer la fenetre tkinter
boutonQuit.pack(side="bottom",padx=5, pady=5)
boutonPlay=Button(canevas, text ='Nouvelle Partie', command=NouvellePartie)#permet d'executer la fonction NouvellePartie
boutonPlay.pack(side="bottom",padx=5, pady=5)

#Protections--------------------------------------------
nbre_protections=4
posY_protections=y1-50
largeur_protections=1.5*largeur_vaisseau #la largeur de la protection s'adapte à la largeur du vaisseau
hauteur_protections=15
resistance_protections=5 #nombre de vie de la protection

#Vies et Score--------------------------------
Vies=3 #nombre de vie du joueur
Score=0 #score du joueur
viesLabel=Label(fenetre, text = "Vies :"+str(Vies), bg="orange") #affiche la vie du joueur dans la zone de jeu
viesLabel.place(x=10, y=10)
scoreLabel=Label(fenetre, text="Score :"+str(Score), bg="orange") #affiche le score du joueur dans la zone de jeu
scoreLabel.place(x=60, y=10)

fenetre.mainloop()
fenetre.destroy()

#lien github : https://github.com/MatthieuPettex/Space-Invader



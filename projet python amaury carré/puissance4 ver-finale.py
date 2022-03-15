# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:19:23 2020

@author: amaury
"""
#importation du module
from tkinter import *


k=[0]

class Joueur ():
    def __init__(self,image,lettre):
        """définition de la classe joueur"""
        self.__image=image #associe à un jouer une image de pion
        self.__score=0  #score du joueur
        self.__lettre=lettre #lettre associé au joueur (ça sert pour la grille)

    def getlettre(self):
        """retourne la lettre du joueur"""
        return self.__lettre

    def getimage(self):
        """retourne l'image du pion du joueur"""
        return self.__image


class cadrillage():
    def __init__(self,image,lcase,lmarge,joueur=[]):
        """ definition de la classe cadriallage"""
        self.__image=image #image du cadriallage
        self.__grille=[["X","X","X","X","X","X"],
                       ["X","X","X","X","X","X"],  #c'est le puissance dans le programme sous forme de liste
                       ["X","X","X","X","X","X"],
                       ["X","X","X","X","X","X"],
                       ["X","X","X","X","X","X"],
                       ["X","X","X","X","X","X"],
                       ["X","X","X","X","X","X"]]
        self.__lcase=lcase #la largeur des cases du cadriallage
        self.__lmarge=lmarge #la marge qui a sur les côté du cardriallage
        self.__joueur=joueur #une liste de 2 joueur

    def pion(self,joueur,x):
        """affiche le pion du joueur à la colone voulu"""
        c=0
        n=(x-self.__lmarge)//self.__lcase     # 50 est la taille d'une collone
        while c<7 :
            if self.__grille[n][c]=="X":
                self.__grille[n].pop(c)
                self.__grille[n].insert(c,self.__joueur[joueur].getlettre())
                dessin.create_image(self.__lcase*n+self.__lcase/2+self.__lmarge,
                                    self.__lcase*6-self.__lcase*c-self.__lcase/2,
                                    image=self.__joueur[joueur].getimage())
                break
            c=c+1

    def puissance4(self,joueur):
        """regarde si 4 pion son aligné"""
        lettre=self.__joueur[joueur].getlettre()
        c=0
        for i in range(7):
            for j in range(6):
                if not self.__grille[i][j]==lettre:
                    c=0
                else:
                    c=c+1
                if c==4:
                    print("Victoire")
                    txt = dessin.create_text(299, 250, text="Victoire", font="Arial 16 italic", fill="black")


        c=0
        for i in range(6):
            for j in range(7):
                if not self.__grille[j][i]==lettre:
                    c=0
                else:
                    c=c+1
                if c==4:
                    print("Victoire")
                    txt = dessin.create_text(299, 250, text="Victoire", font="Arial 16 italic", fill="black")

        c=0
        for i in range(3):
            c=0
            for j in range(4):
                c=0
                for x in range(4):
                    if not self.__grille[j+x][i+x]==lettre:
                        c=0
                    else:
                        c=c+1
                    if c==4:
                        print("Victoire")
                        txt = dessin.create_text(299, 250, text="Victoire", font="Arial 16 italic", fill="black")

        for i in range(3):
           c=0
           for j in range(4):
               c=0
               for x in range(4):
                    if not self.__grille[6-j-x][i+x]==lettre:
                        c=0
                    else:
                        c=c+1
                    if c==4:
                        print("Victoire")
                        txt = dessin.create_text(299, 250, text="Victoire", font="Arial 16 italic", fill="black")


def active(event):
    """fonction qui s'active quand on appui sur le clic gauche"""
    P.pion(k[-1],event.x)
    P.puissance4(k[-1])
    if k[-1]==0:
        k.append(1)
    else:
        k.append(0)
#-----------affichage---------------------------------------------#
#----------fenetre---------------------------------------------------#
fen=Tk()
fen.geometry('600x500')

#---------------------canvas-------------------------------------#
dessin= Canvas(fen,width=600,height=500, bg="white")
dessin.place(x=-1,y=-1)

#------------------------------import des image--------------------------#
pionJ=PhotoImage(file="pion_jaune.gif")
pionR=PhotoImage(file="pion_rouge.gif")
quadrillage=PhotoImage(file="quadrillage.gif")
dessin.create_image(300,250,image=quadrillage)

dessin.bind('<Button-1>',active)

#---------------initialisation des joueurs et du cadriallage --------------------------#
J1=Joueur(pionJ,"L")
J2=Joueur(pionR,"R")
P=cadrillage(quadrillage,80,20,[J2,J1])

fen.mainloop()
try:
    fen.destroy()
except TclError:
    pass

"""mail:limane@cpe.fr"""

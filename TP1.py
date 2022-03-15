# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
"""exo 2
jour = int(input ("entrer le jour : "))
mois = int(input ("entrer le mois : "))
annee = int(input ("entrer l'année : "))

if ValiditeDate(jour, mois,annee) == True:
    print("Date valide")
else:
    print("Date non Valide")
    
def bissextile (annee) :
    if annee % 400 ==0:
        return(True)
    else:
        return(False)

def NombreJourMois (numeroMois, annee) :
    Liste_31j =[1,3,5,7,8,10,10]
    Liste_30j = [4,6,9,11]
    nombreJour =0
    if numeroMois == 2:
        if bissextile(annee) == True:
            nombreJour=28
        else:
            nombreJour=29
    for i in Liste_31j:
        if i == numeroMois:
            nombreJour=31
    for j in Liste_30j:
        if j == numeroMois:
            nombreJour=30
    return(nombreJour)


def ValiditeDate (jour, Numeromois, annee):
    BonJour=NombreJourMois(Numeromois,annee)
    if Numeromois > 12:
        return(False)
    if BonJour >= jour:
        return(True)
    if BonJour < jour:
        return(False)
"""
"""exo3
revenu=eval(input("combien avez vous gagné cette année ? "))

def mesImpots(revenu):
     impots=0
     if revenu < 9964 :
         impots=0
     elif revenu > 9964 and revenu < 27519:
         impots=(revenu-9964)*(14/100)
     elif revenu < 73779 and revenu > 27519:
         impots=((revenu-27519)*(30/100))+((27519-9964)*(14/100))
     elif revenu < 156244 and revenu > 73779:
         impots=((revenu-73779)*(41/100))+((73779-27519)*(30/100))+((27519-9964)*(14/100))
     else :
         impots=((revenu-156244)*(45/100))+((156244-73779)*(41/100))+((73779-27519)*(30/100))+((27519-9964)*(14/100))
     print(impots)
         
mesImpots(revenu)
"""
"""exo4
def multiplication (B,C):
    A=[[],[],[]]
    for i in [0,1,2]:
        L1 = B[0][i]C[i][0]
        L2 = B[1][i]C[i][1]
        L3 = B[2][i]*C[i][2]

        A[0].append(L1) 
        A[1].append(L2) 
        A[2].append(L3) 
    return (A)

B=[[1,2,3],[4,5,6],[7,8,9]]
C=[[1,2,3],[4,5,6],[7,8,9]]
print("A =" , multiplication(B,C))
[11:26 AM]
"""
"""exo5
def ToursHanoi(NmbrPalet, tour1, tour2, tour3,compteur):
    compteur = compteur+1
    print(compteur)
    if NmbrPalet > 0:
        ToursHanoi(NmbrPalet-1,tour1, tour3, tour2,compteur)
        print("déplacer le disque du plot",tour1 , "vers le plot ", tour3)
        ToursHanoi(NmbrPalet-1,tour2, tour1, tour3,compteur)

ToursHanoi(5,1,2,3,0)
"""
"""exo6
nombre=eval(input("nombre entier naturel : "))

def syracuse(nombre):
    Lsyr=[nombre]                     
    while Lsyr[-1] != 1:           
        if Lsyr[-1] % 2 == 0:      
            Lsyr.append(Lsyr[-1]//2)  
        else:                     
            Lsyr.append(Lsyr[-1]*3+1)

    return Lsyr
        
print(syracuse(nombre))  
    
Lsyr=syracuse(nombre)

def maxsyr(Lsyr):
    maxi = Lsyr[0]
    for i in Lsyr:
        if i >= maxi:
            maxi = i
    return maxi
    
print(maxsyr(Lsyr))
    
def temps_vol(nombre):
     return len(syracuse(nombre))-1
    
print(temps_vol(nombre)) 

def dernierIndiceMaximum(liste):
    maxi = liste[0]
    longueur=len(liste)
    indice_max = 0
    for i in range(longueur):
        if liste[i] >= maxi:
            maxi = liste[i]
            indice_max = i
    return indice_max

def vol_max_syr():
    L=[]
    for i in range(1,1000):
        T=temps_vol(i)
        L.append(T)
        i=i+1
    res=dernierIndiceMaximum(L)+1
    return "temps de vol max atteind par",res

print(vol_max_syr())
      
def alt_max_syr():
    L=[]
    for i in range(1,1000):
        x=syracuse(i)
        alt=maxsyr(x)
        L.append(alt)
        i=i+1
    res=dernierIndiceMaximum(L)+1
    return "alt max atteind par",res    
        
print(alt_max_syr())   
"""
nombre=eval(input("nombre entier tricolore ? "))

def booléenne_tricolore(nombre):
    tri=nombre**2
    L=str(tri)
    print(L)
        
booléenne_tricolore(nombre)      
    
    
    
    







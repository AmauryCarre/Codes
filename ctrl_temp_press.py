# Dec 2019
"""
Groupe B: Carré Amaury et Pettex Matthieu
Etat : non fini mais opérationel
Problème : le message de l'activité du chauffage ne s'affiche pas et je ne sais pas pourquoi
           alors que pour la pompe pas de problème
Avancement : - toutes les variables globales sont maintenant des values
             - on a réalisé 4 process gérant le régulateur 
"""
"""
 effacer ecran
 dessiner un cadre 
 * Tache screen :
    - lire val température
    - lire val pression
    - afficher les états
    
* Tache capteur temp : ...
* Tache capteur pression :
* Tache ctrl : 
    - lire val température
    - lire val pression
    - Si Temp > Consigne : déclancher Chauffage sinon eteindre
    - Si pression > Consigne : déclancher Pompe sinon eteindre
    
 ------------------------------
 |                            |
 |  * Température :           |
 |   - consigne : 21          |
 |   - actuelle : 20          |
 |                            |
 |  * Pression :              |
 |   - consigne : 2           |
 |   - actuelle : 20          |
 |                            |
 |  * Etat Chauffage : on     |
 |  * Etat Pompe : off        |
 |  * Relation T / P :        |
 |                            |
 ------------------------------ 
 """

CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


#-------------------------------------------------------
import os, time,math, random, sys
from array import array  # Attention : différent des 'Array' des Process
import os

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def erase_current_line():
    print(CLEARELN, end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')


#============ Constantes d'affichage ====
x_coin_H_G_cadre, y_coin_H_G_cadre= 5, 10
x_coin_B_G_cadre, y_coin_B_G_cadre= 22, 10
x_coin_H_G_Temperature, y_coin_H_G_Temperature= 7, 12
x_coin_H_G_Pression, y_coin_H_G_Pression= 12, 12
x_coin_H_G_Chauffage, y_coin_H_G_Chauffage= 17, 12
x_coin_H_G_Pompe, y_coin_H_G_Pompe= 18, 12
x_coin_H_G_relation_T_P, y_coin_H_G_relation_T_P= 20, 12


# Partie trace et messages :
# 'Nom tache' : [ligne_mess, col_mess]
dict_messages_des_taches={'tache_controleur_central : Pompe' : [25,1], 
                          'tache_controleur_central : Chauffage' : [26,1],
                          'tache_capteur_temperature' : [26,1],
                          'tache_capteur_pression' : [27,1]
                          #'tache_screen' :[28,1]
                          }

ligne_prompt_systeme, col_prompt_systeme= 30,1
relation_entre_T_et_P_courte="P.V = n.8,3.T"
relation_entre_T_et_P_longue="Pression_en_Pa * Volume_en_m3 = nb_molécules * 8.31441 * Temp_en_C"
# avec R = 8,31441 [J/mol.K ] , T en [K] , V en [m3] , p en [Pa], n en [mol]

nb_traits=35
ligne_traits="-"*nb_traits
une_ligne_vid_avec_barres="|"+(" "*(nb_traits-2))+"|"

# Les constantes 
max_temperature_possible=40.0
min_temperature_possible=-10.0
max_pression_possible=200.0
min_pression_possible=50.0 

Temp_init=20.0
Pression_init=115.0
chauffage_init_on=False
Pompe_init_on=True
Cste_Consigne_Temperature=22.0
Cste_Consigne_Pression=117.0

Cste_Alpha=0.345642         # 0.02 # On a P = T * Alpha et T=P/alpha

import multiprocessing as mp
from multiprocessing import Process, Value, Lock
import random, time,math

def ecrire_um_message(nom_tache, mess) :
    ligne_messages, col_messages=dict_messages_des_taches[nom_tache]
    move_to(ligne_messages, col_messages) 
    erase_current_line()
    move_to(ligne_messages, col_messages) 
    print("Tache ", nom_tache, " : ", mess)    
    
def placer_le_cadre() :
    effacer_ecran()
    move_to(x_coin_H_G_cadre, y_coin_H_G_cadre) 
    print(ligne_traits)
    for i in range(17) :
        move_to(x_coin_H_G_cadre+i+1, y_coin_H_G_cadre) 
        print(une_ligne_vid_avec_barres)
    move_to(x_coin_B_G_cadre, y_coin_B_G_cadre) 
    print(ligne_traits)    
    
def ecrire_donnees_temp(val_consigne = 21.0, val_actuelle = 0.0):
    move_to(x_coin_H_G_Temperature, y_coin_H_G_Temperature) 
    print("* Température ")
    move_to(x_coin_H_G_Temperature+1, y_coin_H_G_Temperature+3) 
    print("-Consigne : ", round(val_consigne,2))
    move_to(x_coin_H_G_Temperature+2, y_coin_H_G_Temperature+3) 
    print("-Actuel : ", round(val_actuelle,2)   )
    
def ecrire_donnees_pression(val_consigne = 2.0, val_actuelle = 0.0):
    move_to(x_coin_H_G_Pression, y_coin_H_G_Pression)
    print("* Pression ")
    move_to(x_coin_H_G_Pression+1, y_coin_H_G_Pression+3) 
    print("-Consigne : ", val_consigne)
    #===================================================
    # Lien T et P    
    #val_pression = (val_temperature.value + 273.15) * Cste_Alpha
    move_to(x_coin_H_G_Pression+2, y_coin_H_G_Pression+3) 
    print("-Actuel : ", round(val_actuelle,2))       
  
def ecrire_etats_T_P_et_rel_TP(chauffage_is_on=False, pompe_is_on=False) :
    move_to(x_coin_H_G_Chauffage, y_coin_H_G_Chauffage) 
    print("* Etat Chauffage :", "True " if chauffage_is_on else "False") 
    move_to(x_coin_H_G_Pompe, y_coin_H_G_Pompe) 
    print("* Etat Pompe :", "True " if pompe_is_on else "False")   
    move_to(x_coin_H_G_relation_T_P, y_coin_H_G_relation_T_P) 
    print("* Relation T/P :", relation_entre_T_et_P_courte) 
 
#------------- Les taches / processus -------------------------
def tache_capteur_pression() :  
    # La pression
    if (not pompe_is_on.value) : # on augmente la température de 10% par unité de temps   
        val_pression.value -=1 # KPa
    else :
        val_pression.value += 0.7 # 10% par unité de temps c'est beaucoup trop
    ecrire_um_message("tache_capteur_pression", "Pompe allumée" if pompe_is_on.value else "Pompe eteinte")
    
def tache_capteur_temperature() :    
    delta=0.0                #===================================================
    # Lien T et P    
    #val_pression = (val_temperature.value + 273.15) * Cste_Alpha
    if (not chauffage_is_on.value) : # on baisse la température de 0.1 par seconde
        delta=0.5-random.random()
        if delta > 0 : 
            delta=-0.3
            val_temperature.value+=delta            
    else :
        delta=0.5   #pour atteindre vite le seuil
        val_temperature.value+=delta   
    ecrire_um_message("tache_capteur_temperature", "Chauffage allumé" if chauffage_is_on.value else "Chauffage eteint")  
        
        
def tache_screen() :
 
    ecrire_donnees_temp(Cste_Consigne_Temperature, val_temperature.value)
    ecrire_donnees_pression(Cste_Consigne_Pression, val_pression.value)
    ecrire_etats_T_P_et_rel_TP(chauffage_is_on.value, pompe_is_on.value) 


def tache_controleur_central():  
    
    if (Cste_Consigne_Temperature > val_temperature.value) : chauffage_is_on.value=True
        # if ( not value_Chauffage_on) :chauffage_is_on=Truechauffage_is_on=True
        
    else : chauffage_is_on.value=False # consigne_temperature  <=  val_temperature
        # if (chauffage_is_on) :  chauffage_is_on=Fal"j'eteints"se
            
    if (Cste_Consigne_Pression > val_pression.value) : pompe_is_on.value=True
        # if ( not value_Chauffage_on) :chauffage_is_on=Truechauffage_is_on=True
        
    else : pompe_is_on.value=False # consigne_temperature  <=  val_temperature
        # if (chauffage_is_on) :  chauffage_is_on=False    
    
    if (val_temperature.value >= max_temperature_possible) :
        val_temperature.value = max_temperature_possible
        chauffage_is_on.value=False
    if (val_temperature.value < min_temperature_possible) :
        val_temperature.value = min_temperature_possible
        chauffage_is_on.value=True      #===================================================
    # Lien T et P    
    #val_pression = (val_temperature.value + 273.15) * Cste_Alpha
        
    if (val_pression.value >= max_pression_possible) :
        val_pression.value = max_pression_possible
        pompe_is_on.value=False
    if (val_pression.value < min_pression_possible) :
        val_pression.value = min_pression_possible
        pompe_is_on.value=True  
        
    
    #===================================================
    # Lien T et P    
    #val_pression = (val_temperature.value + 273.15) * Cste_Alpha
    #===================================================
   
    #process qui affiche les informations à l'extérieur du cadre
    PompeProc=Process(target=ecrire_um_message, args=("tache_controleur_central : Pompe" , " --> Activée" if pompe_is_on.value else "--> Désactivée"))
    PompeProc.start()
    ChauffageProc=Process(target=ecrire_um_message,args=("tache_controleur_central : Chauffage", " --> Activé" if chauffage_is_on.value else "--> Désactivé"))
    ChauffageProc.start()
    
    
if __name__ == "__main__" :
    mutex = Lock()

    #val_temperature=Temp_init
    val_temperature = mp.Value('f', Temp_init)
    val_pression = mp.Value('f',Pression_init)
    chauffage_is_on = mp.Value('b',chauffage_init_on)
    pompe_is_on = mp.Value('b',Pompe_init_on)

    #process qui affiche le cadre et les informations à l'intérieur
    ScreenTemp = Process(target=placer_le_cadre)
    ScreenTemp.start()
    Ptemp = Process(target=ecrire_donnees_temp)
    Ptemp.start()
    Ppression = Process(target=ecrire_donnees_pression)
    Ppression.start()
    Petat = Process(target=ecrire_etats_T_P_et_rel_TP)
    Petat.start()

    ScreenTemp.join()
    Ptemp.join()
    Ppression.join()
    Petat.join()
    
    #placer_le_cadre()
    #ecrire_donnees_temp()
    #ecrire_donnees_pression()
    #ecrire_etats_T_P_et_rel_TP()
    liste_process=[]

    curseur_invisible()


    tache_screen() # Première appel pour la mise en place des affichages
    while True : 
        tache_capteur_temperature()
        tache_capteur_pression()
        tache_controleur_central()
        tache_screen()

        try : time.sleep(1)
        except : 
            os.system("tset;reset") 
            raise SystemExit('On sort')

    curseur_visible()
    
    # Fin
    move_to(ligne_prompt_systeme, col_prompt_systeme)
    os.system("tset;reset") 
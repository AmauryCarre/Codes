"""
Groupe B - Carré Pettex
Etat : Fini
Attention : Agrandisser la fenetre du terminal
"""
# Juin 2019
# Cours hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagant, ... ...
# Sans mutex écran

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


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

from multiprocessing import Process, Value, Lock, Array
import os, time,math, random, sys
from array import array  # Attention : différent des 'Array' des Process

keep_running=Value('b',True) # Fin de la course ?
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')


def un_cheval(ma_ligne : int) : # ma_ligne commence à 0
    #move_to(20, 1); print("Le cheval ", chr(ord('A')+ma_ligne), " démarre ...")
    col=1
    #global positions_chevaux

    while col < LONGEUR_COURSE and keep_running.value :
        with mutex:                  # remplace acquire et release
            move_to(ma_ligne+1,col)  # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
            print('\(^o^)/ '+chr(ord('A')+ma_ligne)+'')
        mutex_positions.acquire()
        positions_chevaux[ma_ligne]=col #permet de récupérer la position de chaque cheval 
        mutex_positions.release()
        col+=1
        time.sleep(0.05 * random.randint(1,5))

def arbitre(Nb_process, Pari):
    
    while keep_running.value:       
        mutex_positions.acquire()
        index_cheval_en_tête = 0
        chevalvainceur=0
        index_cheval_perdant = LONGEUR_COURSE-1
        chevalperdant=0

        for i in range(Nb_process):
          if positions_chevaux[i] > index_cheval_en_tête : #Compare la postion du cheval d'indice i à la position du cheval en tete
            index_cheval_en_tête = positions_chevaux[i] #Récupère la position du cheval en tête
            chevalvainceur = i #Récupère le numéro du cheval en tete
     
          if positions_chevaux[i] < index_cheval_perdant : #Compare la postion du cheval d'indice i à la position du dernier cheval 
            index_cheval_perdant = positions_chevaux[i] #Récupère la position du dernier cheval
            chevalperdant = i #Récupère le numéro du dernier cheval
        mutex_positions.release()
        
        move_to(Nb_process+7, 1)
        erase_line_from_beg_to_curs()
        print("le cheval en tête est",'\(^o^)/ '+chr(ord('A')+chevalvainceur))
        
        move_to(Nb_process+8, 1)
        erase_line_from_beg_to_curs()
        print("le cheval à la traine est",'\(^o^)/ '+chr(ord('A')+chevalperdant))
        
        if index_cheval_en_tête == LONGEUR_COURSE-1: #Quand le cheval en tête atteint la ligne d'arrivée, la course se fini = nous sortons de la boucle.
          break

    winners = "Cheval vainqueur :"
    mutex_positions.acquire()
    for i in range(Nb_process):
        if positions_chevaux[i] == LONGEUR_COURSE-1 : #Récupère le cheval ayant franchi la ligne d'arrivée
          winners += " " + chr(ord('A')+i)
    mutex_positions.release()
    move_to(Nb_process+12, 1)
    print(winners)
    
    move_to(Nb_process+13, 1)
    print("Votre pari était :",Pari)
    mutex_positions.acquire()
    for i in range(Nb_process):
        if positions_chevaux[i] == LONGEUR_COURSE-1 :
          if Pari == chr(ord('A')+i): #Compare le cheval sur lequel l'utilisateur a parié à celui qui a gagné la course
              print("Vous êtes le boss sérieusement!")
          else: print("Dommage ;(")
    mutex_positions.release()
    
    
#------------------------------------------------

if __name__ == "__main__" :
    Nb_process = 15
    mes_process = [0 for i in range(Nb_process)]
    process_arbitre = 0
    mutex = Lock()   #Nous créons le mutex utilisé dans def un_cheval
    mutex_positions = Lock() #Nous créons le mutex utilisé dans def arbitre
    positions_chevaux = Array('l',range(Nb_process)) #Nous créons une liste partagée qui correspond à la position de chaque cheval
    positions_chevaux[:] = [0 for i in range(Nb_process)] #Nous initialisons toutes les positions à 0 (les chvaux partent de la ligne de départ)

    LONGEUR_COURSE = 100
    effacer_ecran()
    curseur_invisible()

    move_to(Nb_process+16, 1) 
    print("faites vos paris, entrez le nom du cheval : ")
    Pari = str(input()) #Nous donnons la possibilité à l'utilisateur de parier sur le cheval de son choix

    process_arbitre = Process(target=arbitre, args=(Nb_process, Pari))
    process_arbitre.start()

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = Process(target=un_cheval, args= (i,))
        mes_process[i].start()

    move_to(Nb_process+5, 1)
    print("La course est lancé :   LET'S GOOOoooooo!!!")

    for i in range(Nb_process): 
        mes_process[i].join()
    process_arbitre.join()

    move_to(Nb_process+10, 1)
    curseur_visible()
    print("Résultat final :")


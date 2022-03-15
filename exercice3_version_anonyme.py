'''
Etat : Fini
Problème : Compte les -1 en fin de série
Solution : Ajouter +2 au résultat final
'''

'''première version avec les trois process : pipe anonyme'''
import os
from random import randint

'''initialisation de tous les pipes'''
#pipes Séries : entres dans la générations des nb et leur tries
(dfrSeriePair, dfwSeriePair) = os.pipe()
(dfrSerieImpair, dfwSerieImpair) = os.pipe()

#pipes Sommes : entres dans les process sommateur
(dfrSommePair, dfwSommePair) = os.pipe()
(dfrSommeImpair, dfwSommeImpair) = os.pipe()

pid1 = os.fork() #premier fork, père génère les nb

if pid1 != 0 : #process père génère les nb   
    '''on close les os.pipe() non utilisé dans le père'''
    '''on va écrire dans Trie Pair et Trie Impair et lire les sommes'''
    os.close(dfrSeriePair)
    os.close(dfrSerieImpair)
    os.close(dfwSommePair)
    os.close(dfwSommeImpair)
    
    '''génération et trie des nb aux nombres de N'''
    N=10
    for i in range(N):
        nb = randint(0,100)     #les nb vont jusqu'a 100
        if nb % 2 == 0 :        #vérifie si nb est pair
            print("pair",nb)    #pour les tests
            NombrePair = os.write(dfwSeriePair, nb.to_bytes(4,byteorder='little',signed=True))
        else :                  #sinon impair
            print("impair",nb)  #pour les tests
            NombreImpair = os.write(dfwSerieImpair, nb.to_bytes(4,byteorder='little',signed=True))
    
    '''on dépose -1 à la fin des deux listes'''
    FinSerie = -1
    NombrePair = os.write(dfwSeriePair, FinSerie.to_bytes(4,byteorder='little',signed=True))
    NombreImpair = os.write(dfwSerieImpair, FinSerie.to_bytes(4,byteorder='little',signed=True))

    '''on récupère les sommes dans les process fils'''
    ResultatPair = os.read(dfrSommeImpair, 4)
    ResultatImpair = os.read(dfrSommePair, 4)
    TotalSomme = int.from_bytes(ResultatImpair,byteorder='little',signed=True) + int.from_bytes(ResultatPair,byteorder='little',signed=True)
    print("Total est de :",TotalSomme)

else :  
    pid2 = os.fork()
    '''deuxième fork: le père réalise la somme paire et le fils, la somme impaire'''

    if pid2 != 0 : #process père
        '''on close les pipes inutiles'''
        os.close(dfrSommePair)
        os.close(dfwSommePair)
        os.close(dfrSerieImpair)
        os.close(dfwSerieImpair)
        os.close(dfrSommeImpair)
        os.close(dfwSeriePair)
       
        '''On récupère ce qu'il y a dans le pipe TriePaire'''
        SommePair = 0
        TriePair = 0
        while TriePair != -1 : 
            TriePair = os.read(dfrSeriePair, 4)
            TriePair = int.from_bytes(TriePair,byteorder='little',signed=True) 
            SommePair += TriePair
        EnvoieRes = os.write(dfwSommeImpair, SommePair.to_bytes(4,byteorder='little',signed=True))
        print("somme paire:",SommePair)    #test

    else : #process fils
        '''on close les pipes inutiles'''
        os.close(dfrSommePair)
        os.close(dfwSerieImpair)
        os.close(dfrSommeImpair)
        os.close(dfwSeriePair)
       
        '''On récupère ce qu'il y a dans le pipe TrieImpair'''
        SommeImpair = 0
        TrieImpair = 0
        while TrieImpair != -1 : 
            TrieImpair = os.read(dfrSerieImpair, 4) 
            TrieImpair = int.from_bytes(TrieImpair,byteorder='little',signed=True)
            SommeImpair += TrieImpair         
        EnvoieRes = os.write(dfwSommePair, SommeImpair.to_bytes(4,byteorder='little',signed=True))
        print("somme impaire:",SommeImpair)  #test
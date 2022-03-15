import os,sys
from random import randint

(dfrTP, dfwTP) = os.pipe() #Trie paire
(dfrTI, dfwTI) = os.pipe() #Trie impaire
(dfrSI, dfwSI) = os.pipe() #Somme paire
(dfrSP, dfwSP) = os.pipe() #Somme impaire

pid1 = os.fork()


if pid1 != 0 : #proc père   
    """
    On génère les lst de nb et on les envoie en lecture de 2
    pipes différents.
    """ 
    os.close(dfrTP)
    os.close(dfrTI)
    os.close(dfwSI)
    os.close(dfwSP)
    
    N=1000
    for i in range(N):
        nb = randint(0,100)
        if nb % 2 == 0 : #il est pair
            nPair = os.write(dfwTP, nb.to_bytes(4,byteorder='little',signed=True))
        else :
            nImpair = os.write(dfwTI, nb.to_bytes(4,byteorder='little',signed=True))
    end = -1
    nPair = os.write(dfwTP, end.to_bytes(4,byteorder='little',signed=True))
    nImpair = os.write(dfwTI, end.to_bytes(4,byteorder='little',signed=True))

    sommePaireFinale = os.read(dfrSP, 4)
    sommeImpaireFinale = os.read(dfrSI, 4)
    sommeTotale = int.from_bytes(sommeImpaireFinale,byteorder='little',signed=True) + int.from_bytes(sommePaireFinale,byteorder='little',signed=True)
    print("la somme totale est de :",sommeTotale)

else :  
    pid2 = os.fork()
    """
    On se retrouve avec 3 proc en cours : 
            fork1       fork2
    Père    Père !=0    Père != 0 => Utilisé pour GenerateurNb
                        
            Fils = 0    Fils != 0 => Utilisé pour FiltreImpair
                        Fils = 0  => Utilisé pour FiltrePair
    """ 
    if pid2 != 0 : 
        """
        On récupère ce qu'il y a dans le pipe TriePaire
        On appelle le script filtreImpair et on met le résultat
        en écriture du pipe sommePaire
        """
        os.close(dfrSI)
        os.close(dfwSI)
        os.close(dfrTI)
        os.close(dfwTI)
        os.close(dfrSP)
        os.close(dfwTP)
       
        sommePaire = 0
        nPairNonTrie = 0
        while nPairNonTrie != -1 :  
            nPairNonTrie = os.read(dfrTP, 4)
            nPairNonTrie = int.from_bytes(nPairNonTrie,byteorder='little',signed=True) 
            sommePaire += nPairNonTrie
            
        n = os.write(dfwSP, sommePaire.to_bytes(4,byteorder='little',signed=True))

    else : 
        """
        On récupère ce qu'il y a dans le pipe TrieImpair
        On appelle le script filtrePair et on met le résultat
        en écriture du pipe sommeImpaire
        """
        os.close(dfrSI)
        os.close(dfwTI)
        os.close(dfrSP)
        os.close(dfwTP)
       
        sommeImpaire = 0
        nImpairNonTrie = 0
        while nImpairNonTrie != -1 : 
            nImpairNonTrie = os.read(dfrTI, 4) 
            nImpairNonTrie = int.from_bytes(nImpairNonTrie,byteorder='little',signed=True)
            sommeImpaire += nImpairNonTrie
            
        n = os.write(dfwSI, sommeImpaire.to_bytes(4,byteorder='little',signed=True))
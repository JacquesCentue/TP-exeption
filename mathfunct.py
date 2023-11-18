from math import *

def logga(x:int)->float:
    resultat = log(x)
    return resultat

if __name__ == '__main__':
    try :
        chiffre=int(input("entrer la valeur de X :"))
        if chiffre<=0 :
            raise ValueError()
    except ValueError:
        print("X ne peut pas etre inférieur ou égal a 0 ou votre valeur doit etre chiffrée")

    else:
        print(logga(chiffre))
def divEntier(x:int, y:int)->int :
    if y == 0:
        raise ValueError("Y ne peut pas etre egal a 0")
    if y or x <= 0:
        raise ValueError("Y ou X ne peut pas etre négatif")

    if x<y :
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1



def fichier() :
    try :
        with open('test.txt','r') as f:
            for l in f:
                try :

                    l=l.rstrip("\n\r")
                except IOError:
                    print("Erreur d'écriture")
                except FileExistsError:
                    print("le fichier existe deja")
                except PermissionError:
                    print("vous n'avez pas les permissions néssécaires pour ouvrir le fichier")
                else:
                    print(l)

    except FileNotFoundError:
        print("le fichier spécifié n'existe pas")
    finally:
        f.close()


if __name__ == '__main__':


    fichier()
    try :
        x=int(input("entrer la valeur de x : "))
        y=int(input("entrer la valeur de y : "))

    except ValueError:
        print("la valeur doit etre chifrée.")
    else:
        print(divEntier(6, 2))
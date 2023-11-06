def divEntier(x:int, y:int)->int :
    try :

        if y == 0:
            raise ValueError1("Y ne peut pas etre egal a 0")
        if y or x <= 0:
            raise ValueError2("Y ou X ne peut pas etre négatif")
    except ValueError1 :
        print("Y ne peut pas etre egal a 0")
    except ValueError2:
        print("Y ou X ne peut pas etre négatif")
    finally:
        if x<y :
            return 0
        else:
            x = x - y
            return divEntier(x, y) + 1

if __name__ == '__main__':



    try :
        x=int(input("entrer la valeur de x : "))
        y=int(input("entrer la valeur de y : "))

    except ValueError:
        print("la valeur doit etre chifrée.")
    else:
        print(divEntier(6, 2))
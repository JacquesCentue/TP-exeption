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

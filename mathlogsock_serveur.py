import time
import socket
import math
import mathfunct



Host = "0.0.0.0"
Port = 4090

#Creation du socket
socket = socket.socket(socket.AF_INET)
socket.bind((Host,Port))
socket.listen(1)
serverstat=1
print("serveur pret ... ")



#Le script s'arrete jusqu'a une connection
client, ip = socket.accept()

if __name__ == '__main__':
    while serverstat==1 :


        x = client.recv(1024)
        x = x.decode()
        print(x)
        y = client.recv(1024)
        y = y.decode()
        print(y)
        try:
            X=int(x)
            Y=int(y)
            if X <= 0 or Y <=0:
                raise ValueError()
        except ValueError:
            print("X ne peut pas etre inférieur ou égal a 0 ou votre valeur doit etre chiffrée")
            msg="X ne peut pas etre inférieur ou égal a 0 ou votre valeur doit etre chiffrée"
            msg = msg.encode()
            client.send(msg)

        else :
            #calcul des valeurs
            #x
            msg = str(mathfunct.logga(X))
            msg = msg.encode()
            client.send(msg)

            #y
            msg = str(mathfunct.logga(Y))
            msg = msg.encode()
            client.send(msg)

            time.sleep(1)
            socket.close()


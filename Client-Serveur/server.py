from threading import Thread
import socket

def Send(client):
    while True:
        msg = input()
        msg = msg.encode()
        client.send(msg)
def Reception(client):
    while True:
        requete_client = client.recv(1024)
        requete_client = requete_client.decode()
        print(requete_client)
        if not requete_client : #Si on pert la connexion
            print("CLOSE")
            break

Host = "0.0.0.0"
Port = 4090

#Creation du socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket.bind((Host,Port))
socket.listen(1)
print("serveur pret ... ")

#Le script s'arrete jusqu'a une connection
client, ip = socket.accept()
print("Le client d'ip",ip,"se connecte")

envoi = Thread(target=Send,args=[client])
recep = Thread(target=Reception,args=[client])

envoi.start()
recep.start()

recep.join()

client.close()
socket.close()
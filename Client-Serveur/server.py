
<<<<<<< Updated upstream
# -*- coding: latin-1 -*-

import socket # Import socket module

s = socket.socket()
nom_hote = socket.gethostname()
addr_ip_hote = socket.gethostbyname(nom_hote)
=======

def Send(client):
    while True:
        msg = input()
        msg = msg.encode()
        client.send(msg)


def Reception(client):
    while server==1:
        requete_client = client.recv(1024)
        requete_client = requete_client.decode()
        print(requete_client)
        if not requete_client : #Si on pert la connexion
            print("CLOSE")
            break

Host = "0.0.0.0"
Port = 4090
server =1

#Creation du socket
socket = socket.socket(socket.AF_INET)


>>>>>>> Stashed changes


<<<<<<< Updated upstream
port = 4090
s.bind((nom_hote, port))
=======
print("Serveur de test d'envoi de messages")
print("Serveur demarre, en attente d'une connexion ...")

#Le script s'arrete jusqu'a une connection
client, ip = socket.accept()
print("Le client d'ip",ip,"se connecte")
>>>>>>> Stashed changes

print("Serveur de test d'envoi de messages")
print ("->nom du serveur %s"%nom_hote)
print( "->IP de l'hote : %s"%addr_ip_hote)
print( "->port :%i"%port)
print("Serveur démarré, en attente d'une connexion ...")


s.listen(5)


c, addr = s.accept()
addr_ip_client = addr[0]
print("Connection recue depuis le client : ",addr_ip_client)

message="Connecté au serveur !"
c.send(message.encode())

while True:
    msgClient = c.recv(1024)
    print ("C>", msgClient)
    if msgClient.upper()== "FIN" or msgClient == "":
        break
        msgServeur = raw_input("S> ")
        c.send(msgServeur)
# on ferme la connexion
        c.close()

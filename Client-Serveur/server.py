
# -*- coding: latin-1 -*-

import socket # Import socket module

s = socket.socket()
nom_hote = socket.gethostname()
addr_ip_hote = socket.gethostbyname(nom_hote)


port = 4090
s.bind((nom_hote, port))

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

SRVstatus=1
while SRVstatus==1:
    msgClient = c.recv(1024)
    while msgClient!="bye" or msgClient!="arret":
        s.listen(5)
        print ("C>", msgClient)
        msgServeur=msgClient
        c.send(msgClient)
        msgClient = c.recv(1024)

    print("fermeture du serveur")
    SRVstatus=0
c.close()

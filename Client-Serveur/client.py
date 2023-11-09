# -*- coding: latin-1 -*-
import socket


server = socket.socket()


port = 4090
addr_ip = "10.128.6.12"
server.connect((socket.gethostbyaddr(addr_ip)[0], port))


while True:
    print(server.recv(1024))
    server.send("Bonjour ici le client")
    if msgClient.upper()== "FIN" or msgClient == "":
       break
    msgServeur = raw_input("S> ")
    c.send(msgServeur)
    # fermeture du socket
server.close()
from threading import Thread
import socket

def Send(socket):
    while True:
        msg = input("message : ")
        msg = msg.encode()
        socket.send(msg)
def Reception(socket):
    while True:
        requete_server = socket.recv(1024)
        requete_server = requete_server.decode()
        print(requete_server)

Host = "10.128.3.19"
Port = 4090

#Creation du socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((Host,Port))

envoi = Thread(target=Send,args=[socket])
recep = Thread(target=Reception,args=[socket])

envoi.start()
recep.start()
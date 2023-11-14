
import socket

<<<<<<< Updated upstream
=======
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
>>>>>>> Stashed changes

server = socket.socket()


port = 4090
addr_ip = "10.128.1.65"
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
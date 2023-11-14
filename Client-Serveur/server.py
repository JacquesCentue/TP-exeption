from threading import Thread
import socket

def Send(client):

    while True:
        msg = input()
        msg = msg.encode()
        client.send(msg)
def Reception(client):
    server =1
    while server == 1:
        requete_client = client.recv(1024)
        requete_client = requete_client.decode()
        print(requete_client)
        if requete_client=="bye" or requete_client=="arret":
            socket.close()



Host = "0.0.0.0"
Port = 4090

#Creation du socket
socket = socket.socket(socket.AF_INET)

socket.bind((Host,Port))
socket.listen(5)

print("serveur pret ... ")



#Le script s'arrete jusqu'a une connection
client, ip = socket.accept()
print("Le client d'ip",ip,"se connecte")
if __name__ == '__main__':
    envoi = Thread(target=Send,args=[client])
    recep = Thread(target=Reception,args=[client])

    envoi.start()
    recep.start()

    recep.join()

    client.close()
    socket.close()
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Configuration du serveur
        self.HOST = '127.0.0.1'
        self.PORT = 55555

        # Liste pour stocker les connexions des clients
        self.clients = []

        # Création du socket serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        # Créer un thread pour écouter les connexions
        threading.Thread(target=self.listen_connections).start()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Serveur de chat')

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

    def listen_connections(self):
        while True:
            # Accepter une connexion client
            client_socket, address = self.server_socket.accept()

            # Ajouter le client à la liste
            self.clients.append((client_socket, address))

            # Créer un thread pour gérer le client
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def handle_client(self, client_socket, address):
        while True:
            try:
                # Réception du message du client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                # Diffusion du message à tous les clients
                self.broadcast(message, address)
            except:
                # En cas d'erreur, fermer la connexion du client
                self.remove_client(client_socket)
                break

    def broadcast(self, message, sender_address):
        # Diffusion du message à tous les clients
        for client in self.clients:
            try:
                # Envoi du message à chaque client sauf l'expéditeur

                    client[0].send(message.encode('utf-8'))
            except:
                # En cas d'erreur, fermer la connexion du client
                self.remove_client(client[0])

    def remove_client(self, client_socket):
        # Retirer un client de la liste
        for client in self.clients:
            #si le client correspont au socket de la liste client, on ferme son socket
            if client[0] == client_socket:
                self.clients.remove(client)
                break

if __name__ == '__main__':
    app = QApplication([])
    server_window = ServerWindow()
    server_window.show()
    app.exec_()

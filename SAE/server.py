
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QMainWindow, QGridLayout, QLabel, QLineEdit, QComboBox, QTextEdit
import socket
import setuptools
import threading
import os
import platform
import sys
import shutil
from PyQt5.QtCore import *



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de chat")
        self.resize(300, 400)
        self.setup_ui()
        self.clients = []

            

    def setup_ui(self):
        self.label = QLabel("Serveur")
        self.tbxHost = QLineEdit("127.0.0.1")
        self.lblPort = QLabel("Port")
        self.tbxPort = QLineEdit("4090")
        self.button = QPushButton("Démarrer le serveur")
        self.lblMaxClient = QLabel("Nombre maximum de clients")
        self.tbxnbMaxHost = QLineEdit("5")
        self.tbxChat = QTextEdit()
        self.tbxChat.setReadOnly(True)

        self.button.clicked.connect(self.demarrer_serveur)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.tbxHost, 0, 1)
        layout.addWidget(self.lblPort, 1, 0)
        layout.addWidget(self.tbxPort, 1, 1)
        layout.addWidget(self.lblMaxClient, 2, 0)
        layout.addWidget(self.tbxnbMaxHost, 2, 1)
        layout.addWidget(self.button, 3, 0, 1, 3)
        layout.addWidget(self.tbxChat, 4, 0, 1, 3)
        self.setLayout(layout)


    def demarrer_serveur(self):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind(("0.0.0.0", int(self.tbxPort.text())))
        self.serveur.listen(int(self.tbxnbMaxHost.text()))
        # self.button.setEnabled(True)
        self.button.setText("Arrêter le serveur")
        self.label.setText("Serveur démarré")
        self.button.clicked.connect(self.arreter_serveur)
        self.lblPort.setText("Attente de connexion")
        self.lblMaxClient.setText("Nombre de clients connectés : 0")
        self.thread_ecoute = threading.Thread(target=self.ecoute)
        self.thread_ecoute.start()

    def arreter_serveur(self):
        self.serveur.close()
        self.label.setText("Serveur")
        self.lblPort.setText("Port")
        self.lblMaxClient.setText("Nombre maximum de clients")
        self.button.clicked.connect(self.demarrer_serveur)
        self.button.setEnabled(True)
        self.tbxChat.clear()


    def ecoute(self):
        while True:
            self.connexion, self.adresse = self.serveur.accept()
            self.lblPort.setText("Connexion établie avec {}".format(self.adresse))
            self.clients.append((client_socket, address))
            self.thread_reception = threading.Thread(target=self.reception)
            self.thread_reception.start()

    def reception(self):
        while True:
            try:
                # Réception du message du client
                self.message_recu = self.connexion.recv(1024).decode('utf-8')
                if not message:
                    break
                if self.message_recu == "Jacques> no":
                    print("clearing")
                    self.tbxChat.clear()
                self.tbxChat.append(self.message_recu)
                self.lblMaxClient.setText("Nombre de clients connectés : {}".format(len(threading.enumerate()) - 2))
                self.connexion.send(self.message_recu.encode())
                print(self.message_recu.encode())
                # Diffusion du message à tous les clients
                broadcast(message)
            except:
                # En cas d'erreur, fermer la connexion du client
                remove_client(client_socket)
                break

    def broadcast(message):
        for client in clients:
            try:
                # Envoi du message à chaque client sauf l'expéditeur
                if client[1] != sender_address:
                    client[0].send(message.encode('utf-8'))
            except:
                # En cas d'erreur, fermer la connexion du client
                remove_client(client[0])






        
    

if __name__ == "__main__":

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QMainWindow, QGridLayout, QLabel, QLineEdit, QComboBox, QTextEdit
import socket
import setuptools
import psutil
import netaddr
import netifaces
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
            

    def setup_ui(self):
        self.label = QLabel("Serveur")
        self.line_edit = QLineEdit("127.0.0.1")
        self.label2 = QLabel("Port")
        self.line_edit2 = QLineEdit("10000")
        self.button = QPushButton("Démarrer le serveur")
        self.label3 = QLabel("Nombre maximum de clients")
        self.line_edit3 = QLineEdit("5")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.button.clicked.connect(self.demarrer_serveur)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.line_edit, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.line_edit2, 1, 1)
        layout.addWidget(self.label3, 2, 0)
        layout.addWidget(self.line_edit3, 2, 1)
        layout.addWidget(self.button, 3, 0, 1, 3)
        layout.addWidget(self.text_edit, 4, 0, 1, 3)
        self.setLayout(layout)


    def demarrer_serveur(self):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind((self.line_edit.text(), int(self.line_edit2.text())))
        self.serveur.listen(int(self.line_edit3.text()))
        # self.button.setEnabled(True)
        self.button.setText("Arrêter le serveur")
        self.label.setText("Serveur démarré")
        self.button.clicked.connect(self.arreter_serveur)
        self.label2.setText("Attente de connexion")
        self.label3.setText("Nombre de clients connectés : 0")
        self.thread_ecoute = threading.Thread(target=self.ecoute)
        self.thread_ecoute.start()

    def arreter_serveur(self):
        self.serveur.close()
        self.label.setText("Serveur")
        self.label2.setText("Port")
        self.label3.setText("Nombre maximum de clients")
        self.button.clicked.connect(self.demarrer_serveur)
        self.button.setEnabled(True)
        self.text_edit.clear()


    def ecoute(self):
        while True:
            self.connexion, self.adresse = self.serveur.accept()
            self.label2.setText("Connexion établie avec {}".format(self.adresse))
            self.thread_reception = threading.Thread(target=self.reception)
            self.thread_reception.start()

    def reception(self):
        while True:
            self.message_recu = self.connexion.recv(1024).decode()
            self.text_edit.append(self.message_recu)
            self.label3.setText("Nombre de clients connectés : {}".format(len(threading.enumerate())-2))
        
    

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

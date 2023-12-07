import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555

        # Configuration du socket client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        # Créer un thread pour gérer la réception des messages
        threading.Thread(target=self.receive_messages).start()

    def initUI(self):
        self.setGeometry(500, 100, 400, 400)
        self.setWindowTitle('Client de chat')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.input_line = QLineEdit(self)
        self.send_button = QPushButton('Envoyer', self)
        self.send_button.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.input_line)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def receive_messages(self):
        while True:
            try:
                # Réception du message du serveur
                message = self.client_socket.recv(1024).decode('utf-8')
                self.text_edit.append(message)
            except:
                # En cas d'erreur, fermer la connexion du client
                print("Erreur lors de la réception du message.")
                self.client_socket.close()
                break

    def send_message(self):
        # Envoi du message au serveur
        message = self.input_line.text()
        self.client_socket.send(message.encode('utf-8'))
        self.input_line.clear()

if __name__ == '__main__':
    app = QApplication([])
    client_window = ClientWindow()
    client_window.show()
    app.exec_()

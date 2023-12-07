import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, \
    QDialog, QMessageBox
import socket
import threading


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555
        self.utilisateur = None
        self.channel = None

        # Afficher la fenêtre d'authentification au lancement de l'application
        self.show_auth_window()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Authentification')

        self.label_username = QLabel('Nom d\'utilisateur:', self)
        self.label_password = QLabel('Mot de passe:', self)

        self.input_username = QLineEdit(self)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Se connecter', self)
        self.login_button.clicked.connect(self.authenticate_user)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def show_auth_window(self):
        self.show()

    def authenticate_user(self):
        try:
            # Envoyer le nom d'utilisateur et le mot de passe au serveur pour l'authentification
            username = self.input_username.text()
            password = self.input_password.text()

            # Envoyer le nom d'utilisateur et le mot de passe au serveur
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))

            # Obligation de mettre un délai entre la connexion au socket et l'envoi des messages sinon la fenêtre est bloquée (test)
            time.sleep(0.5)
            self.client_socket.send(username.encode('utf-8'))
            self.client_socket.send(password.encode('utf-8'))

            # Recevoir la réponse du serveur
            response = self.client_socket.recv(1024).decode('utf-8')
            if response.startswith("AUTHORIZED"):
                # Analyser la réponse pour obtenir le numéro d'utilisateur et les droits d'accès, séparé par une virgule
                _, utilisateur, droits = response.split(',')
                self.utilisateur = utilisateur
                self.channel = int(droits)

                # Fermer la fenêtre d'authentification et afficher la fenêtre principale
                self.accept()
            else:
                # Afficher un message d'erreur en cas d'authentification échouée
                QMessageBox.critical(self, 'Erreur d\'authentification',
                                     'Accès refusé. Veuillez vérifier vos informations.')
                self.client_socket.close()

        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")

    def get_credentials(self):
        return self.utilisateur, self.channel


class ChatWindow(QMainWindow):
    def __init__(self, utilisateur, channel, password):
        super().__init__()

        self.initUI()

        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555
        self.utilisateur = utilisateur
        self.channel = channel
        self.password = password

        # Connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        time.sleep(0.5)
        # Envoyer le numéro d'utilisateur et les droits d'accès au serveur une deuxième fois
        self.client_socket.send(str(self.utilisateur).encode('utf-8'))
        self.client_socket.send(str(self.password).encode('utf-8'))

        # Créer un thread pour gérer la réception des messages, l'envoi se situe dans le thread principal
        threading.Thread(target=self.receive_messages).start()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Chat Multi-canaux')

        self.lblChat = QLabel("chat")
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.input_line = QLineEdit(self)
        self.send_button = QPushButton('Envoyer', self)
        self.send_button.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.lblChat)
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
        message = (f"{self.utilisateur}> {self.input_line.text()}")

        self.client_socket.send(message.encode('utf-8'))
        self.text_edit.append(f"vous> {message}")
        self.input_line.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    if auth_window.exec() == QDialog.Accepted:
        utilisateur, channel = auth_window.get_credentials()
        client_window = ChatWindow(utilisateur, channel, auth_window.input_password.text())
        client_window.show()
        sys.exit(app.exec_())

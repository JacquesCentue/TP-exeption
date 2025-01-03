import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, \
    QDialog, QMessageBox, QComboBox, QMenu, QAction
from PyQt5.QtGui import QKeySequence
import socket
import threading
import cryptocode
import hashlib


class AuthWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555
        self.utilisateur = None
        self.droits = None

        # Afficher la fenêtre d'authentification au lancement de l'application
        self.show_auth_window()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Authentification')

        self.lblUsername = QLabel('Nom d\'utilisateur:', self)
        self.lblPassword = QLabel('Mot de passe:', self)

        self.tbxUsername = QLineEdit(self)
        self.tbxPassword = QLineEdit(self)
        self.tbxPassword.setEchoMode(QLineEdit.Password)

        self.btnLogin = QPushButton('Se connecter', self)
        self.btnLogin.clicked.connect(self.authenticate_user)

        layout = QVBoxLayout()
        layout.addWidget(self.lblUsername)
        layout.addWidget(self.tbxUsername)
        layout.addWidget(self.lblPassword)
        layout.addWidget(self.tbxPassword)
        layout.addWidget(self.btnLogin)

        self.setLayout(layout)

    def show_auth_window(self):
        self.show()

    def authenticate_user(self):
        try:
            # Envoyer le nom d'utilisateur et le mot de passe au serveur pour l'authentification
            username = self.tbxUsername.text()
            password = self.tbxPassword.text()
            # password= cryptocode.encrypt(password, "zabchat")
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            print(password)

            # Envoyer le nom d'utilisateur et le mot de passe au serveur
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))

            # Obligation de mettre un délai entre la connexion au socket et l'envoi des messages sinon la fenêtre est bloquée (test)
            time.sleep(0.5)
            self.client_socket.send(username.encode('utf-8'))
            self.client_socket.send(password.encode('utf-8'))

            # Recevoir la réponse du serveur
            response = self.client_socket.recv(1024).decode('utf-8')
            response = cryptocode.decrypt(response, "uhgkO4SG5SETzgs54e/ù")

            # si le message  commance avec "AUTHORIZED" on accepte la boite de dialogue
            if response.startswith("AUTHORIZED"):
                # Analyser la réponse pour obtenir le numéro d'utilisateur et les droits d'accès, séparé par une virgule
                _, userid, utilisateur, droits = response.split(',')
                self.userid = userid
                self.utilisateur = utilisateur
                self.droits = int(droits)

                # Fermer la fenêtre d'authentification et afficher la fenêtre principale
                self.accept()
            elif response.startswith("BANNED"):
                QMessageBox.critical(self, 'Erreur d\'authentification',
                                     'Accès refusé. Vous avez été banni veuillez contacter un administrateur')
                self.client_socket.close()
            else:
                # Afficher un message d'erreur en cas d'authentification échouée
                QMessageBox.critical(self, 'Erreur d\'authentification',
                                     'Accès refusé. Veuillez vérifier vos informations.')
                self.client_socket.close()

        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")

    def get_credentials(self):
        '''
        cette classe va retourner au programme principal en envoyant un tuple de 3 parametres
        :return: self.userid, self.utilisateur, self.droits
        '''
        return self.userid, self.utilisateur, self.droits


class ChangePasswordWindow(QDialog):
    '''
    classe qui permet d'afficher une fenetre de changement de mot de passe de l'utilisateur déjà connecté
    '''

    def __init__(self, utilisateur, client_socket):
        '''
        constructeur de la classe qui permet de changer de mot de passe
        :param utilisateur:
        :param client_socket:
        '''
        super().__init__()

        self.initUI()
        self.utilisateur = utilisateur
        self.client_socket = client_socket

    def initUI(self):
        '''
        Fonction qui permet de définir les éléments de l'interface utilisateur
        :return: void
        '''
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Changer le mot de passe')

        self.lblNouvMDP = QLabel('Nouveau mot de passe:', self)
        self.tbxNouvMDP = QLineEdit(self)
        self.tbxNouvMDP.setEchoMode(QLineEdit.Password)

        self.lblConfirm = QLabel('Confirmer le mot de passe:', self)
        self.tbxConfirm = QLineEdit(self)
        self.tbxConfirm.setEchoMode(QLineEdit.Password)

        self.btnChangerMDP = QPushButton('Changer le mot de passe', self)
        self.btnChangerMDP.clicked.connect(self.change_password)

        layout = QVBoxLayout()
        layout.addWidget(self.lblNouvMDP)
        layout.addWidget(self.tbxNouvMDP)
        layout.addWidget(self.lblConfirm)
        layout.addWidget(self.tbxConfirm)
        layout.addWidget(self.btnChangerMDP)

        self.setLayout(layout)

    def change_password(self):
        '''
        fonction qui permet de changer le mot de passe de l'utilisateur il faut que les 2 mots de passe soient identiques
        :return:
        '''
        new_password = self.tbxNouvMDP.text()
        confirm_password = self.tbxConfirm.text()

        # Vérifiez que les mots de passe correspondent
        if new_password == confirm_password:
            try:
                new_password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
                # Envoyez le nouvel utilisateur et le mot de passe au serveur pour la mise à jour
                message = f"/ChangePassword {self.utilisateur} {new_password}"
                message = cryptocode.encrypt(message, "earg45rsy72zerg")
                self.client_socket.send(message.encode('utf-8'))

                # Attendez la réponse du serveur
                response = self.client_socket.recv(1024).decode('utf-8')

                if response.startswith("/PasswordChanged"):
                    # Mot de passe changé avec succès
                    QMessageBox.information(self, 'Changement de mot de passe', 'Mot de passe changé avec succès!')
                    self.accept()
                else:
                    QMessageBox.critical(self, 'Erreur', 'Échec du changement de mot de passe.')
            except Exception as e:
                print(f"Erreur lors du changement de mot de passe: {e}")
        else:
            QMessageBox.critical(self, 'Erreur', 'Les mots de passe ne correspondent pas.')


class ChatWindow(QMainWindow):
    def __init__(self, userid, utilisateur, droits, password):
        '''
        constructeur de la classe ChatWindow
        :param userid: id d'utilisateur
        :param utilisateur: nom d'utilisateur
        :param droits: droits d'utilisateur ce qui permet d'affiches les canaux auquel il a accès
        :param password: mot de passe de l'utilisateur
        '''
        super().__init__()

        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555
        self.userid = userid
        self.utilisateur = utilisateur
        self.droits = droits
        self.password = password
        self.initUI()
        self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        time.sleep(0.5)
        # Envoyer le numéro d'utilisateur et les droits d'accès au serveur une deuxième fois
        self.client_socket.send(str(self.utilisateur).encode('utf-8'))
        self.client_socket.send(str(self.password).encode('utf-8'))
        time.sleep(1)
        # Créer un thread pour gérer la réception des messages, l'envoi se situe dans le thread principal
        threading.Thread(target=self.receive_messages).start()

        self.createActions()
        self.createMenuBar()

    def createMenuBar(self):
        """
        cette fonction mermet d'afficher le menu option
        :return: void
        """
        menuBar = self.menuBar()

        file = menuBar.addMenu("Option")
        file.addAction(self.actChangePassword)
        file.addAction(self.actExit)

    def createActions(self):
        '''
        cette fonction permettant de faire fonctionner la menu option
        :return: void
        '''
        self.actChangePassword = QAction("Changer de mot de passe", self)
        self.actChangePassword.setShortcut(QKeySequence("Ctrl+P"))
        self.actChangePassword.triggered.connect(self.open_change_password_window)

        self.actExit = QAction("Exit", self)
        self.actExit.setShortcut(QKeySequence("Alt+F4"))
        self.actExit.setStatusTip("Exit")
        # La méthode close est directement fournie par la classe QMainWindow.

        self.actExit.triggered.connect(self.fermeture)

    def fermeture(self):
        '''
        cette fonction est le resultat si l'utilisateur appuie sur exit dans le menu option
        :return: 0
        '''
        self.client_socket.close()
        self.close()
        app.exit(0)
        sys.exit(0)

    def open_change_password_window(self):
        change_password_window = ChangePasswordWindow(self.utilisateur, self.client_socket)
        if change_password_window.exec() == QDialog.Accepted:
            # Vous pouvez ajouter le code ici pour envoyer le nouveau mot de passe au serveur si nécessaire
            print("Mot de passe changé avec succès!")

    def initUI(self):
        '''
        cette fonction permet d'afficher la fenetre
        :return: void
        '''
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Zabchat')

        self.lblChat = QLabel("General")
        self.tbxGeneralChat = QTextEdit(self)
        self.tbxGeneralChat.setReadOnly(True)
        self.tbxGeneralChat.setStyleSheet("background-color: rgb(255, 250, 205);")
        self.tbxGeneralChat.setStyleSheet("color: black;")
        self.tbxGeneralChat.hide()

        self.tbxBlablaChat = QTextEdit(self)
        self.tbxBlablaChat.setReadOnly(True)
        self.tbxBlablaChat.setStyleSheet("background-color: rgb(255, 250, 205);")
        self.tbxBlablaChat.setStyleSheet("color: blue;")
        self.tbxBlablaChat.hide()

        self.tbxInformatiqueChat = QTextEdit(self)
        self.tbxInformatiqueChat.setReadOnly(True)
        self.tbxInformatiqueChat.setStyleSheet("background-color: rgb(255, 250, 205);")
        self.tbxInformatiqueChat.setStyleSheet("color: green;")
        self.tbxInformatiqueChat.hide()

        self.tbxMarketingChat = QTextEdit(self)
        self.tbxMarketingChat.setReadOnly(True)
        self.tbxMarketingChat.setStyleSheet("background-color: rgb(255, 250, 205);")
        self.tbxMarketingChat.setStyleSheet("color: pink;")
        self.tbxMarketingChat.hide()

        self.tbxComptabiliteChat = QTextEdit(self)
        self.tbxComptabiliteChat.setReadOnly(True)
        self.tbxComptabiliteChat.setStyleSheet("background-color: rgb(255, 250, 205);")
        self.tbxComptabiliteChat.setStyleSheet("color: orange;")
        self.tbxComptabiliteChat.hide()

        self.input_line = QLineEdit(self)
        # Envoi du message si l'utilisateur appuie sur la touche entrer
        self.input_line.returnPressed.connect(self.send_message)

        self.send_button = QPushButton('Envoyer', self)
        self.send_button.clicked.connect(self.send_message)

        # definission de la combobox des diférents cannaux
        self.cbxCannaux = QComboBox(self)

        self.selectChat("General")
        self.cbxCannaux.addItem("General")
        self.selectChat(self.lblChat.text())
        self.cbxCannaux.addItem("Blabla")
        if self.droits >= 5:
            self.cbxCannaux.addItem("Informatique")
        if self.droits == 3 or self.droits == 4 or self.droits == 7 or self.droits == 8:
            self.cbxCannaux.addItem("Marketing")
        if self.droits == 2 or self.droits == 4 or self.droits == 6 or self.droits == 8:
            self.cbxCannaux.addItem("Comptabilite")

        self.cbxCannaux.currentTextChanged.connect(self.selectChat)

        # affichage des widgets
        layout = QVBoxLayout()
        layout.addWidget(self.lblChat)
        layout.addWidget(self.cbxCannaux)
        layout.addWidget(self.tbxGeneralChat)
        layout.addWidget(self.tbxBlablaChat)
        layout.addWidget(self.tbxInformatiqueChat)
        layout.addWidget(self.tbxMarketingChat)
        layout.addWidget(self.tbxComptabiliteChat)
        layout.addWidget(self.input_line)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def selectChat(self, value, ):
        '''
        cette fonction permet de determiner le chat selectionné de l'utilisateur
        :param value: valeur de la chaine de caracteres selectionné dans le combobox
        :return: void
        '''
        # print("combobox changed", value)
        self.lblChat.setText(value)
        if self.lblChat.text() == "General":
            self.tbxGeneralChat.show()
            self.tbxBlablaChat.hide()
            self.tbxInformatiqueChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxComptabiliteChat.hide()

        elif self.lblChat.text() == "Blabla":
            self.tbxGeneralChat.hide()
            self.tbxBlablaChat.show()
            self.tbxInformatiqueChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxComptabiliteChat.hide()

        elif self.lblChat.text() == "Informatique":
            self.tbxGeneralChat.hide()
            self.tbxBlablaChat.hide()
            self.tbxInformatiqueChat.show()
            self.tbxMarketingChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxComptabiliteChat.hide()

        elif self.lblChat.text() == "Marketing":
            self.tbxGeneralChat.hide()
            self.tbxBlablaChat.hide()
            self.tbxInformatiqueChat.hide()
            self.tbxMarketingChat.hide()
            self.tbxMarketingChat.show()
            self.tbxComptabiliteChat.hide()

        elif self.lblChat.text() == "Comptabilite":
            try:
                # code de detection de droit -> ceci est le code que j'avais mis en place avant d'avoir mis en place la detection des droits a l'ouverture de la fenetre
                if self.droits == 2 or self.droits == 4 or self.droits == 6 or self.droits == 8:
                    self.tbxGeneralChat.hide()
                    self.tbxBlablaChat.hide()
                    self.tbxInformatiqueChat.hide()
                    self.tbxMarketingChat.hide()
                    self.tbxMarketingChat.hide()
                    self.tbxComptabiliteChat.show()
                else:
                    raise Exception("Désolé, vous n'avez pas les droits")
            except Exception as e:
                QMessageBox.critical(self, 'Erreur lors du changement de cannux',
                                     'Accès refusé. Vous n\'avez pas les droits de consulter ce canal.')
                self.cbxCannaux.removeItem("Comptabilite")

    def receive_messages(self):
        '''
        fonction qui permet de recevoir les messages les messages seront analysés afin de determiner dans quel canal le message appartient
        :return:
        '''
        client_status = 1
        while client_status == 1:

            try:
                # print(self.droits)
                # Réception du message du serveur
                message = self.client_socket.recv(1024).decode('utf-8')
                # on décrypte le message avec un mot de passe
                message = cryptocode.decrypt(message, "uhgkO4SG5SETzgs54e/ù")

                # on determine a quel cannal le message apartient
                if message.startswith("/Blabla"):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxBlablaChat.append(messagetransmi)
                elif message.startswith("/Informatique") and (
                        self.droits == 5 or self.droits == 6 or self.droits == 7 or self.droits == 8):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxInformatiqueChat.append(messagetransmi)
                elif message.startswith("/Marketing") and (
                        self.droits == 3 or self.droits == 4 or self.droits == 7 or self.droits == 8):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxMarketingChat.append(messagetransmi)
                elif message.startswith("/Comptabilite") and (
                        self.droits == 2 or self.droits == 4 or self.droits == 6 or self.droits == 8):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxComptabiliteChat.append(messagetransmi)
                elif message.startswith("/General"):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxGeneralChat.append(messagetransmi)
                elif message.startswith("AUTHORIZED") or message.startswith("/ChangePassword"):

                    print(message)
                elif message == "QUIT":
                    self.client_socket.close()
                    app.exit(0)
                    sys.exit(0)

                else:
                    self.tbxGeneralChat.append(message)


            except Exception as e:
                # En cas d'erreur, fermer la connexion du client
                print(f"Erreur lors de la réception du message. {e}")
                self.client_socket.close()
                client_status = 0

    def send_message(self):
        '''
        fonction qui permet d'envoyer les messages au serveur
        :return: void
        '''
        # Envoi du message au serveur
        message = self.input_line.text().strip()
        # verification du contenu du message (si il n'est pas vide)
        if message != "":
            if message != "bye":

                message = (f"/{self.lblChat.text()} {self.utilisateur}> {self.input_line.text()}")
                # on chiffre le message afin qu'il soi cachés aux clients frauduleux
                message = cryptocode.encrypt(message, "earg45rsy72zerg")
                # print(message)
                self.client_socket.send(message.encode('utf-8'))
                # self.tbxGeneralChat.append(f"vous> {message}")

                self.input_line.clear()
            else:
                message = ("bye")
                message = cryptocode.encrypt(message, "earg45rsy72zerg")
                self.client_socket.send(message.encode('utf-8'))
                time.sleep(0.5)
                self.client_socket.close()
                app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    if auth_window.exec() == QDialog.Accepted:
        userid, utilisateur, droits = auth_window.get_credentials()
        client_window = ChatWindow(userid, utilisateur, droits, auth_window.tbxPassword.text())
        client_window.show()
        sys.exit(app.exec_())
        sys.exit(0)


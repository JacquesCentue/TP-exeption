import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, \
    QDialog, QMessageBox,QComboBox
import socket
import threading
import cryptocode

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
            #password= cryptocode.encrypt(password, "zabchat")
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
            if response.startswith("AUTHORIZED"):
                # Analyser la réponse pour obtenir le numéro d'utilisateur et les droits d'accès, séparé par une virgule
                _,userid, utilisateur, droits = response.split(',')
                self.userid = userid
                self.utilisateur = utilisateur
                self.droits = int(droits)

                # Fermer la fenêtre d'authentification et afficher la fenêtre principale
                self.accept()
            elif response.startswith("BANNED"):
                QMessageBox.critical(self, 'Erreur d\'authentification', 'Accès refusé. Vous avez été banni veuillez contacter un administrateur')
                self.client_socket.close()
            else:
                # Afficher un message d'erreur en cas d'authentification échouée
                QMessageBox.critical(self, 'Erreur d\'authentification','Accès refusé. Veuillez vérifier vos informations.')
                self.client_socket.close()

        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")

    def get_credentials(self):
        return self.userid, self.utilisateur, self.droits


class ChatWindow(QMainWindow):
    def __init__(self,userid, utilisateur, droits, password):
        super().__init__()



        # Configuration du client
        self.HOST = '127.0.0.1'
        self.PORT = 55555
        self.userid=userid
        self.utilisateur = utilisateur
        self.droits = droits
        self.password = password
        self.initUI()

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

    def initUI(self):
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

        #definission de la combobox des diférents cannaux
        self.cbxCannaux = QComboBox(self)

        self.selectChat("General")
        self.cbxCannaux.addItem("General")
        self.selectChat(self.lblChat.text())
        self.cbxCannaux.addItem("Blabla")
        if self.droits >= 5:
            self.cbxCannaux.addItem("Informatique")
        if self.droits ==3 or self.droits==4 or self.droits==7 or self.droits==8 :
            self.cbxCannaux.addItem("Marketing")
        if self.droits == 2 or self.droits == 4 or self.droits == 6 or self.droits == 8:
            self.cbxCannaux.addItem("Comptabilite")



        self.cbxCannaux.currentTextChanged.connect(self.selectChat)

        #affichage des widgets
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

    def selectChat(self, value,):
        print("combobox changed", value)
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
                #code de detection de droit -> ceci est le code que j'avais mis en place avant d'avoir mis en place la detection des droits a l'ouverture de la fenetre
                if self.droits== 2 or self.droits==4 or self.droits==6 or self.droits==8:
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
        client_status=1
        while client_status==1:
            try:
                print(self.droits)
                # Réception du message du serveur
                message = self.client_socket.recv(1024).decode('utf-8')

                if message.startswith("/Blabla"):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxBlablaChat.append(messagetransmi)
                elif message.startswith("/Informatique") and self.droits <= 5:
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxInformatiqueChat.append(messagetransmi)
                elif message.startswith("/Marketing") and (self.droits ==3 or self.droits==4 or self.droits==7 or self.droits==8):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxMarketingChat.append(messagetransmi)
                elif message.startswith("/Comptabilite") and (self.droits== 2 or self.droits==4 or self.droits==6 or self.droits==8):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxComptabiliteChat.append(messagetransmi)
                elif message.startswith("/General"):
                    messagetransmi = message.split()
                    messagetransmi = ' '.join(messagetransmi[1:])
                    self.tbxGeneralChat.append(messagetransmi)
                elif message.startswith("AUTHORIZED"):
                    message = (f"{self.utilisateur} s'est connecté")

                    self.client_socket.send(message.encode('utf-8'))
                    print(message)
                elif message == "QUIT":
                    print("QUIT")
                    ChatWindow.close(self)
                    socket.close(self)
                else:
                    self.tbxGeneralChat.append(message)


            except Exception as e:
                # En cas d'erreur, fermer la connexion du client
                print(f"Erreur lors de la réception du message. {e}")
                self.client_socket.close()
                break

    def send_message(self):
        # Envoi du message au serveur
        message = self.input_line.text().strip()
        # verification du contenu du message (si il n'est pas vide)
        if message != "":
            if message !="bye":


                message = (f"/{self.lblChat.text()} {self.utilisateur}> {self.input_line.text()}")
                #print(message)
                self.client_socket.send(message.encode('utf-8'))
                #self.tbxGeneralChat.append(f"vous> {message}")


                self.input_line.clear()
            else:
                message = ("bye")

                self.client_socket.send(message.encode('utf-8'))
                time.sleep(0.5)
                self.client_socket.close()
                app.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    if auth_window.exec() == QDialog.Accepted:
        userid, utilisateur, droits = auth_window.get_credentials()
        client_window = ChatWindow(userid,utilisateur, droits, auth_window.input_password.text())
        client_window.show()
        sys.exit(app.exec_())

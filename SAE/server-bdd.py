import socket
import threading
import mysql.connector
import time
import sys,os
import cryptocode
import datetime


class Server:
    def __init__(self):
        # Configuration du serveur
        self.HOST = '0.0.0.0'
        self.PORT = 55555
        self.serverstatus=1
        # Connexion à la base de données MySQL
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='zabchat',
            password='zabchat',
            database='zabchat'
        )
        self.clients = []

        # Création du socket serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.ban = []




        # Créer un thread pour écouter les connexions
        threading.Thread(target=self.listen_connections).start()

        #démarage du thread de commande permettant l'administration du serveur
        threading.Thread(target=self.commande()).start()

    def listen_connections(self):
        """
        fonction permettant d'ecouter en continu grace au thread si un client souhaite se connecter.
        :return:
        """
        while self.serverstatus==1:
            # Accepter une connexion client
            client_socket, client_address = self.server_socket.accept()

            # Ajouter le client à la liste
            self.clients.append((client_socket, client_address))

            # Créer un thread pour gérer le client
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        '''
        fonction petmettant au serveur d'authentifier le client et de recevoir les message des clients afin de les diffuser a tout le monde

        :param client_socket: objet de type socket ayant tout les parametres du socket du client tel que son addresse, son port,...
        :param client_address: liste contenant l'adresse ip et le port utilisé pour la communication
        :return:
        '''
        #print(f"client_socket {client_socket}")
        #print(f"client_address {client_address}")
        try:
            #on raffraichit la liste des utilisateurs et des ip bannies lorsqu'un autre utilisateur se connecte
            self.ban =[]

            # creation de la liste des utilisateurs bannis
            cursor = self.db_connection.cursor(buffered=True)
            cursor.execute("SELECT ban FROM ban WHERE  dateUnban > NOW()")
            # Cela permet le formatage de la liste a partir des identifiants, on enleve les parentheses
            self.ban = [user[0] for user in cursor.fetchall()]

            """print(f"utilisateurs bannis : {self.ban}")
            for i in range(len(self.ban)):
                print(f"utilisateur banni {i} : {self.ban[i]}")
            print(self.ban)"""
            cursor.close()




            # Réception du nom d'utilisateur et du mot de passe du client
            username = client_socket.recv(1024).decode('utf-8')
            password = client_socket.recv(1024).decode('utf-8')

            #test de passage des identifiants
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT user_id,username, rights FROM user WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            cursor.close()


            i=0
            for i in range(len(self.ban)):
                if username != self.ban[i] and client_address[0]!=self.ban[i]:
                    continu=1

                else:
                    client_socket.send("BANNED".encode('utf-8'))
                    print(f"une utilisateur banni a tenté une connexion : {self.ban[i]}")
                    # Fermer la connexion du client
                    username = ""

                    client_socket.close()

            self.ban = []

            if user:
                userid, username, access_rights = user
                # Envoyer l'autorisation au client avec le numéro d'utilisateur et les droits d'accès
                #print(f"AUTHORIZED,{userid},{username},{access_rights}")
                client_socket.send(f"AUTHORIZED,{userid},{username},{access_rights}".encode('utf-8'))
                self.broadcast(f"/General {username} s'est connecté", "0.0.0.0")



                        # Attendre les messages du client
                while self.serverstatus==1:


                    #print(f"userid:{userid}")
                    try:
                        message = client_socket.recv(1024).decode('utf-8')

                        #print(message) # debug afin de voir si le message arrive jusque la
                        if message =="bye":
                            self.broadcast(f"/General {username} s'est déconnecté", "0.0.0.0")

                            self.remove_client(client_socket)

                        # Diffusion du message à tous les clients
                        self.broadcast(message, client_address)
                        #print(client_address) #affichage de debug

                        # Ecriture du message dans le base de donnée pour modération
                        cursor = self.db_connection.cursor()
                        cursor.execute("INSERT INTO generalchat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",(userid,message,client_address[0]))
                        self.db_connection.commit()
                        cursor.close()

                    except Exception as e:
                        # En cas d'erreur, fermer la connexion du client
                        print(e)
                        self.remove_client(client_socket)
                        break

            else:
                # Envoi d'une autorisation refusée au client
                client_socket.send("UNAUTHORIZED".encode('utf-8'))

                # Fermer la connexion du client
                client_socket.close()


        except Exception as e:
            print(f"Erreur lors du traitement du client : {e}")




    def broadcast(self, message, sender_address):
        '''
        fonction permettant d'envoyer les message a chaque client
        :param message: message a envoyer a tous les utilisateurs
        :param sender_address: adresse ip de l'expéditeur
        :return:
        '''
        # Diffusion du message à tous les clients
        for client in self.clients:
            try:
                # Envoi du message à chaque client meme a l'expéditeur afin de voir si la connexion au serveur est active
                    client[0].send(message.encode('utf-8'))
            except:
                # En cas d'erreur, fermer la connexion du client
                self.remove_client(client[0])

    def remove_client(self, client_socket):
        '''
        fonction permettant de supprimer des client en cas de problèmes ou si le client se déconnecte.
        :param client_socket: objet de la classe socket.socket stockant les parametres du client
        :return:
        '''
        # Retirer un client de la liste

        for client in self.clients:
            # si le client correspont au socket de la liste client, on ferme son socket
            if client[0] == client_socket:

                self.clients.remove(client)


    def commande(self):
        '''
        fonction permettant a l'administrateur d'écrire des commandes afin d'administer le serveur
        :return:
        '''
        serverStatus = 1
        print(f"/help ou /? pour afficher l'aide")
        while serverStatus==1:
            commandPrompt = input("root : ")
            if commandPrompt=="/shutdown":

                self.broadcast("vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                time.sleep(60)
                for client_socket, _ in self.clients:
                    try:
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                    except Exception as e:
                        print(f"Erreur lors du shutdown : {e}")

                try:
                    # Fermer le socket serveur
                    self.server_socket.shutdown(socket.SHUT_RDWR)
                    self.server_socket.close()
                except Exception as e:
                    print(f"erreur lors de l'extinction du serveur {e}")
                self.serverStatus =0

            elif commandPrompt.startswith("/ban"):
                username = commandPrompt.split()[1]

                try:
                    arg2 = commandPrompt.split()[2]  # Prend le deuxième argument

                    # Ajoute l'utilisateur à la liste des bannis avec le deuxième argument
                    cursor = self.db_connection.cursor()
                    cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (username,))
                    cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (arg2,))
                    self.db_connection.commit()
                    cursor.close()
                    for client in self.clients:
                        if client[1][0] == arg2 and client[1][0] != self.client_address[0]:  # Comparaison avec l'adresse IP
                            # Si l'adresse IP est connectée et n'est pas celle de l'administrateur, déconnecte le client
                            client[0].send("bye".encode('utf-8'))
                            self.remove_client(client[0])
                            print(f"Déconnexion de l'utilisateur avec l'adresse IP {arg2}")

                except IndexError:
                    # Si aucun deuxième argument n'est fourni
                    cursor = self.db_connection.cursor()
                    cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (username,))
                    self.db_connection.commit()
                    cursor.close()
                    print(f"Bannissement de {username}")
                except Exception as e:
                    print(f"Erreur lors du bannissement : {e}")


            elif commandPrompt.startswith("/unban"):
                username = commandPrompt.split()[1]

                try:
                    # Supprime l'utilisateur de la liste des bannis
                    cursor = self.db_connection.cursor()
                    cursor.execute("DELETE FROM ban WHERE ban.ban =%s", (username,))
                    self.db_connection.commit()
                    cursor.close()
                    print(f"l'utilisateur {username} a été gracié")

                except Exception as e:
                    print(f"Erreur lors du traitement de la commande : {e}")


            elif commandPrompt.startswith("/send"):
                message=commandPrompt.split()
                message = "/General serveur > "+' '.join(message[1:])
                self.broadcast(message,"0.0.0.0")

            elif commandPrompt.startswith("/kick"):
                username = commandPrompt.split()[1]

                try:

                    arg2 = int(commandPrompt.split()[2] ) # Prend le deuxième argument
                    dateUnban = datetime.datetime.now() + datetime.timedelta(days=arg2)
                    print(dateUnban)

                    # Ajoute l'utilisateur à la liste des bannis avec le deuxième argument
                    cursor = self.db_connection.cursor()
                    cursor.execute("INSERT INTO ban(ban, dateban, dateUnban) VALUES (%s, NOW(), %s)",(username, dateUnban))
                    self.db_connection.commit()
                    cursor.close()
                    print(f"L'utilisateur {username} a été privé de communication pour {arg2} jours jusqu'au {dateUnban}")
                    for client in self.clients:
                        if client[1][0] == arg2:  # Comparaison avec l'adresse IP
                            # Si l'adresse IP est connectée, déconnecte le client
                            client[0].send("bye".encode('utf-8'))
                            self.remove_client(client[0])
                            print(f"Déconnexion de l'utilisateur avec l'adresse IP {arg2}")
                except IndexError:
                    dateUnban = datetime.datetime.now() + datetime.timedelta(days=1)
                    # Si aucun deuxième argument n'est fourni
                    cursor = self.db_connection.cursor()
                    cursor.execute("INSERT INTO ban(ban, dateban, dateUnban) VALUES (%s, NOW(), %s)",(username, dateUnban))
                    self.db_connection.commit()
                    cursor.close()
                    print(f"L'utilisateur {username} a été privé de communication pour 1 jour")
                except Exception as e:
                    print(f"Erreur lors du Timeout : {e}")

            elif commandPrompt=="/help" or commandPrompt == "/?":
                print("voici la liste des commandes :\n"
                      "- /help permet d'afficher la liste des commandes disponibles\n"
                      "- /ban <arg1> <arg2>(optionnel) permet de bannir un utilisateur et son adresse ip\n"
                      "- /unban <arg1> permet de grâcier un utilisateur banni\n"
                      "- /send <message> permet d'envoyer un message via le serveur\n"
                      "- /kick <utilisateur> <jour(s)> permet de bannir temporairement un utilisateur/help")

            else:
                print("commande inconnue")


if __name__ == '__main__':
    serverstatus=1
    while serverstatus==1:
        server = Server()
        serverstatus=Server()


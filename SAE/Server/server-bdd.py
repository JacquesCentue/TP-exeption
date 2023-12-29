import socket
import threading
import mysql.connector
import time
import sys,os
import cryptocode
import datetime
import hashlib


class Server:
    def __init__(self):
        '''
        constructeur de la classe serveur, permet d'initialiser toutes les variables
        '''
        # Configuration du serveur
        self.HOST = '0.0.0.0'
        self.PORT = 55555
        self.serverstatus=1
        # Connexion à la base de données MySQL
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='zabchat',
            password='sdfghjkl',
            database='zabchat'
        )

        #liste de tous les clients connectés
        self.clients = []

        # Création du socket serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        # liste des utilisateur/IP bannis
        self.ban = []

        self.mdpRoot="4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2"


        # Créer un thread pour écouter les connexions
        threading.Thread(target=self.listen_connections).start()

        #démarage du thread de commande permettant l'administration du serveur
        threading.Thread(target=self.commande()).start()

    def listen_connections(self):
        """
        fonction permettant d'ecouter les nouvelles connections en continu grâce au thread si un client souhaite se connecter.
        :return: void
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
        et ecriture du message dans la base de donnée dans la table correspondante au canal

        :param client_socket: objet de type socket ayant tout les parametres du socket du client tel que son addresse, son port,...
        :param client_address: liste contenant l'adresse ip et le port utilisé pour la communication
        :return: void
        '''

        try:
            #on raffraichit la liste des utilisateurs et des ip bannies lorsqu'un autre utilisateur se connecte
            self.ban =[]

            # creation de la liste des utilisateurs bannis
            cursor = self.db_connection.cursor(buffered=True)
            cursor.execute("SELECT ban FROM ban WHERE  dateUnban > NOW()")
            # Cela permet le formatage de la liste a partir des identifiants, on enleve les parentheses
            self.ban = [user[0] for user in cursor.fetchall()]

            #test pour voir la liste des utilisateurs /ip bannis
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
                    client_socket.send(cryptocode.encrypt("BANNED", "uhgkO4SG5SETzgs54e/ù").encode('utf-8'))
                    print(f"un utilisateur banni a tenté une connexion : {self.ban[i]}")
                    # Fermer la connexion du client
                    username = ""

                    client_socket.close()

            self.ban = []

            if user:
                userid, username, access_rights = user
                # Envoyer l'autorisation au client avec le numéro d'utilisateur et les droits d'accès
                #print(f"AUTHORIZED,{userid},{username},{access_rights}")
                client_socket.send(cryptocode.encrypt(f"AUTHORIZED,{userid},{username},{access_rights}\n", "uhgkO4SG5SETzgs54e/ù").encode('utf-8'))
                time.sleep(0.5)
                self.broadcast(f"{username} s'est connecté", "0.0.0.0")



                        # Attendre les messages du client
                while self.serverstatus==1:


                    #print(f"userid:{userid}")
                    try:
                        message = client_socket.recv(1024).decode('utf-8')
                        #print(f"message recu avant décryptage : {message}")
                        message = cryptocode.decrypt(message, "earg45rsy72zerg")
                        #print(f"message recu après décryptage : {message}")
                        messagerecu=message.split()



                        #print(message) # debug afin de voir si le message arrive jusque la
                        if message =="bye":
                            self.broadcast(f"{username} s'est déconnecté", "0.0.0.0")

                            self.remove_client(client_socket)

                        # Diffusion du message à tous les clients
                        self.broadcast(message, client_address)
                        #print(client_address) #affichage de debug

                        # debut de la séquence de test afin d'ecrire le message dans la base de données dans la table correspondante au canal de chat
                        if message.startswith("/General") :
                            messagerecu = ' '.join(messagerecu[1:])
                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO generalchat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",(userid,messagerecu,client_address[0]))
                            self.db_connection.commit()
                            cursor.close()
                        elif message.startswith("/Blabla"):
                            messagerecu = ' '.join(messagerecu[1:])
                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO blablachat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",(userid, messagerecu, client_address[0]))
                            self.db_connection.commit()
                            cursor.close()
                        elif message.startswith("/Informatique"):
                            messagerecu = ' '.join(messagerecu[1:])
                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO infochat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",
                                           (userid, messagerecu, client_address[0]))
                            self.db_connection.commit()
                            cursor.close()
                        elif message.startswith("/Marketing"):
                            messagerecu = ' '.join(messagerecu[1:])
                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO marketingchat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",
                                           (userid, messagerecu, client_address[0]))
                            self.db_connection.commit()
                            cursor.close()
                        elif message.startswith("/Comptabilite"):
                            messagerecu = ' '.join(messagerecu[1:])
                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO comptachat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",
                                           (userid, messagerecu, client_address[0]))
                            self.db_connection.commit()
                            cursor.close()
                        elif message.startswith("/ChangePassword"):

                            cursor = self.db_connection.cursor()
                            cursor.execute("UPDATE `user` SET `password` = %s WHERE `user`.`username` = %s",(messagerecu[2],messagerecu[1]))
                            self.db_connection.commit()
                            cursor.close()
                            print(f"l'utilisateur {messagerecu[1]} a changé de mot de passe: {messagerecu[2]}")
                            client_socket.send("/PasswordChanged".encode('utf-8'))

                        else :

                            # Ecriture du message dans le base de donnée pour modération
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO generalchat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",
                                           (userid, message, client_address[0]))
                            self.db_connection.commit()
                            cursor.close()

                    except Exception as e:
                        # En cas d'erreur ou si le client ferme la fenetre, fermer la connexion du client
                        #print(f"le client {client_address[0]} s'est déconnecté ")
                        self.remove_client(client_socket)
                        break

            else:
                # Envoi d'une autorisation refusée au client
                client_socket.send(cryptocode.encrypt("UNAUTHORIZED", "uhgkO4SG5SETzgs54e/ù").encode('utf-8'))

                # Fermer la connexion du client
                client_socket.close()


        except Exception as e:
            print(f"Erreur lors du traitement du client : {e}")




    def broadcast(self, message, sender_address):
        '''
        fonction permettant d'envoyer les message a chaque client
        :param message: message a envoyer a tous les utilisateurs
        :param sender_address: adresse ip de l'expéditeur
        :return: void
        '''
        #print(f"message avant cryptage: {message}")
        message = cryptocode.encrypt(message, "uhgkO4SG5SETzgs54e/ù")
        #print(f"message crypté: {message}")
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
        :return: void
        '''
        # Retirer un client de la liste

        for client in self.clients:
            # si le client correspont au socket de la liste client, on ferme son socket
            if client[0] == client_socket:

                self.clients.remove(client)


    def commande(self):
        '''
        fonction permettant a l'administrateur d'écrire des commandes afin d'administer le serveur de chat
        l'administrateur effecue les commandes via la console python pour voir la liste des commandes: "/help" ou "/?"
        :return: void
        '''

        serverStatus = 1
        mdp=hashlib.sha256(input("Mot de Passe d'administration :").encode("utf-8")).hexdigest()
        if mdp==self.mdpRoot:

            print(f"/help ou /? pour afficher l'aide")
            while serverStatus==1:
                commandPrompt = input("root : ")
                try :
                    command= commandPrompt.split()[0]
                    if commandPrompt=="/shutdown":
                        #on est obligé de faire un delai entre chaque message sinon tout les message se retrouvent dans Blabla
                        self.broadcast("vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                        time.sleep(0.5)
                        self.broadcast("/Blabla vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                        time.sleep(0.5)
                        self.broadcast("/Informatique vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                        time.sleep(0.5)
                        self.broadcast("/Marketing vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                        time.sleep(0.5)
                        self.broadcast("/Comptabilite vous allez etre déconnecté dans 1 minute (le serveur va s'arreter)", "0.0.0.0")
                        time.sleep(60)

                        print("Arrêt du serveur en cours...")
                        # Fermer tous les sockets clients
                        for client_socket, _ in self.clients:
                            try:
                                client_socket.send(cryptocode.encrypt("QUIT", "uhgkO4SG5SETzgs54e/ù").encode('utf-8'))
                                client_socket.shutdown(socket.SHUT_RDWR)
                                client_socket.close()
                            except Exception as e:
                                print(f"Erreur lors du shutdown : {e}")

                        # Fermer le socket serveur
                        try:
                            self.server_socket.shutdown(socket.SHUT_RDWR)
                            self.server_socket.close()
                            print("Serveur déconnecté")
                        except Exception as e:
                            print(f"Erreur lors de l'extinction du serveur {e}")
                        os.close(1)

                        # Arrêter le thread de commande
                        self.serverstatus = 0
                        quit()

                        print("Serveur arrêté")

                    elif command=="/ban":
                        username = commandPrompt.split()[1]

                        try:
                            arg2 = commandPrompt.split()[2]  # Prend le deuxième argument

                            # Ajoute l'utilisateur à la liste des bannis avec le deuxième argument
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (username,))
                            cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (arg2,))
                            self.db_connection.commit()
                            cursor.close()
                            print(f"{username} et {arg2} on été bannis")
                            

                        except IndexError:
                            # Si aucun deuxième argument n'est fourni
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (username,))
                            self.db_connection.commit()
                            cursor.close()
                            print(f"Bannissement de {username}")
                        except Exception as e:
                            print(f"Erreur lors du bannissement : {e}")


                    elif command=="/unban":
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


                    elif command=="/send":
                        try:
                            message=commandPrompt.split()
                            message = ' '.join(message[1:])
                            self.broadcast(message,"0.0.0.0")
                        except Exception as e:
                            print(f"Erreur lors de l'envoi du message : {e}")


                    elif command=="/kick":
                        username = commandPrompt.split()[1]

                        try:
                            try :
                                arg2 = int(commandPrompt.split()[2] ) # Prend le deuxième argument
                                dateUnban = datetime.datetime.now() + datetime.timedelta(days=arg2)
                                print(dateUnban)

                                # Ajoute l'utilisateur à la liste des bannis avec le deuxième argument
                                cursor = self.db_connection.cursor()
                                cursor.execute("INSERT INTO ban(ban, dateban, dateUnban) VALUES (%s, NOW(), %s)",(username, dateUnban))
                                self.db_connection.commit()
                                cursor.close()
                                print(f"L'utilisateur {username} a été privé de communication pour {arg2} jours jusqu'au {dateUnban}")
                            except Exception as e:
                                # nous sommes obligés de faire une update au cax ou l'utilisateur est deja enregistré dans la base de donnée car c'est une clé primaire donc il n'y a pas de duplicata possible
                                arg2 = int(commandPrompt.split()[2])  # Prend le deuxième argument
                                dateUnban = datetime.datetime.now() + datetime.timedelta(days=arg2)


                                cursor = self.db_connection.cursor()
                                cursor.execute("UPDATE `ban` SET `dateban` = NOW(), `dateUnban` = %s WHERE `ban`.`ban` = %s",(dateUnban,username))
                                self.db_connection.commit()
                                cursor.close()
                                print(
                                    f"L'utilisateur {username} a été privé de communication pour {arg2} jours jusqu'au {dateUnban}")


                        except IndexError:
                            try :
                                dateUnban = datetime.datetime.now() + datetime.timedelta(days=1)
                                # Si aucun deuxième argument n'est fourni
                                cursor = self.db_connection.cursor()
                                cursor.execute("INSERT INTO ban(ban, dateban, dateUnban) VALUES (%s, NOW(), %s)",(username,dateUnban ))
                                self.db_connection.commit()
                                cursor.close()
                                print(f"L'utilisateur {username} a été privé de communication pour 1 jour")
                            except Exception as e:
                                print("l\'utilisateur est déjà présent dans la table, modification de la ligne")
                                dateUnban = datetime.datetime.now() + datetime.timedelta(days=1)
                                # Si aucun deuxième argument n'est fourni et que l'utilisateur est déja présent dans la table de bannissement
                                cursor = self.db_connection.cursor()
                                cursor.execute("UPDATE `ban` SET `dateban` = NOW(), `dateUnban` = %s WHERE `ban`.`ban` = %s",(username, dateUnban))
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
                          "- /send /<Canal>(optionnel) <message> permet d'envoyer un message via le serveur\n"
                          "- /kick <utilisateur> <jour(s)> permet de bannir temporairement un utilisateur\n"
                          "- /droit <numero de droit> <utilisateur> permet de changer les droits de l'utilisateur -> droit se fait par rapport au numéro: voir readme\n"
                          "- /createuser <utilisateur> <mot de passe> <numero de droit> permet de créer un utilisateur via la console\n"
                          "- /deluser <utilisateur> permet de supprimer un utilisateur via la console\n"
                          "- /mdp <utilisateur> <mot de passe> permet a l'administrateur de changer le mot de passe depuis la console")

                    elif command=="/droit":
                        try:
                            droits=commandPrompt.split()[1]
                            username = commandPrompt.split()[2]
                            cursor = self.db_connection.cursor()
                            cursor.execute("UPDATE `user` SET `rights` = %s WHERE `user`.`username` = %s",(droits, username))
                            self.db_connection.commit()
                            cursor.close()
                        except Exception as e:
                            print(f"Erreur lors du changement des droits de l'utilisateur : {e}")

                    elif command=="/createuser":
                        try :
                            droits = commandPrompt.split()[3]
                            username = commandPrompt.split()[1]
                            password = commandPrompt.split()[2]
                            password=hashlib.sha256(password.encode("utf-8")).hexdigest()
                            print(password)
                            cursor = self.db_connection.cursor()
                            cursor.execute("INSERT INTO user(username, password, rights) VALUES (%s, %s, %s)",(username,password,droits))
                            self.db_connection.commit()
                            cursor.close()
                            print(f"L'utilisateur {username} est maintenant disponible")

                        except Exception as e:
                            print(f"erreur lors de la création de l'utilisateur : {e}")

                    elif command=="/deluser":
                        try:
                            username = commandPrompt.split()[1]
                            cursor = self.db_connection.cursor()
                            cursor.execute("DELETE FROM user WHERE `user`.`username` = %s",(username,))
                            self.db_connection.commit()
                            cursor.close()
                            print(f"L'utilisateur {username} est maintenant supprimé")
                        except Exception as e:
                            print(f"Erreur lors de la suppression du compte : {e}")



                    elif command=="/mdp":
                        try :
                            username = commandPrompt.split()[1]
                            password = commandPrompt.split()[2]
                            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
                            cursor = self.db_connection.cursor()
                            cursor.execute("UPDATE `user` SET `password` = %s WHERE `user`.`username` = %s", (password, username))
                            self.db_connection.commit()
                            cursor.close()
                        except Exception as e:
                            print(f"Erreur lors du changement de mot de passe : {e}")

                    else:
                        print("commande inconnue")

                except:
                    serverStatus=1
        else :
            print("Authentification echoué veuiller réessayer... etes vous un hacker ?")
            self.commande()

if __name__ == '__main__':

    server = Server()
    sys.exit()



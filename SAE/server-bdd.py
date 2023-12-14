import socket
import threading
import mysql.connector
import time
import sys,os
import cryptocode


class Server:
    def __init__(self):
        # Configuration du serveur
        self.HOST = '0.0.0.0'
        self.PORT = 55555

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

        self.ipban = []
        self.ipuserban = []



        # Créer un thread pour écouter les connexions
        threading.Thread(target=self.listen_connections).start()
        threading.Thread(target=self.commande()).start()

    def listen_connections(self):
        while True:
            # Accepter une connexion client
            client_socket, client_address = self.server_socket.accept()

            # Ajouter le client à la liste
            self.clients.append((client_socket, client_address))

            # Créer un thread pour gérer le client
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        try:
            #on raffraichit la liste des utilisateurs et des ip bannies lorsqu'un autre utilisateur se connecte
            self.ban =[]

            # creation de la liste des utilisateurs bannis
            cursor = self.db_connection.cursor(buffered=True)
            cursor.execute("SELECT ban FROM ban")
            # Cela permet le formatage de la liste a partir des identifiants, on enleve les parentheses
            self.ban = [user[0] for user in cursor.fetchall()]

            #print(f"utilisateurs bannis : {self.ban}")
            #for i in range(len(self.ban)):
            #    print(f"utilisateur banni {i} : {self.ban[i]}")
            #print(self.ban)
            cursor.close()




            # Réception du nom d'utilisateur et du mot de passe du client
            username = client_socket.recv(1024).decode('utf-8')
            password = client_socket.recv(1024).decode('utf-8')

            #test de passage des identifiants
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT user_id,username, rights FROM user WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            # test de debuggage pour verifier l'adresse ip lors d'une connection a distance
            #print(f"adresse ip : {client_address[0]} , port {client_address[1]}")
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



            if user:
                userid, username, access_rights = user
                # Envoyer l'autorisation au client avec le numéro d'utilisateur et les droits d'accès
                #print(f"AUTHORIZED,{userid},{username},{access_rights}")
                client_socket.send(f"AUTHORIZED,{userid},{username},{access_rights}".encode('utf-8'))
                self.broadcast(f"{username} s'est connecté", "0.0.0.0")



                        # Attendre les messages du client
                while True:


                    #print(f"userid:{userid}")
                    try:
                        message = client_socket.recv(1024).decode('utf-8')
                        print(message)
                        if message =="bye":
                            self.broadcast(f"{username} s'est déconnecté", "192.168.154.225")

                            self.remove_client(client_socket)


                        if not message:
                            break

                        # Diffusion du message à tous les clients
                        self.broadcast(message, client_address)
                        print(client_address)
                        # Ecriture du message dans le base de donnée pour modération
                        cursor = self.db_connection.cursor()
                        cursor.execute("INSERT INTO generalchat(idsent,message,ipEnvoi) VALUES (%s,%s,%s)",(userid,message,client_address[0]))
                        user = cursor.fetchone()
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
        # Diffusion du message à tous les clients
        for client in self.clients:
            try:
                # Envoi du message à chaque client sauf l'expéditeur
                #if client[1] != sender_address:
                    client[0].send(message.encode('utf-8'))
            except:
                # En cas d'erreur, fermer la connexion du client
                self.remove_client(client[0])

    def remove_client(self, client_socket):
        # Retirer un client de la liste

        for client in self.clients:
            # si le client correspont au socket de la liste client, on ferme son socket
            if client[0] == client_socket:

                self.clients.remove(client)

                break

    def restart_server(self):
        print("Redémarrage du serveur...")
        self.broadcast("le serveur va redémare dans 10 secondes ","0.0.0.0")
        time.sleep(10)

        # Fermer tous les sockets clients
        for client, _ in self.clients:
            client.close()

        # Fermer le socket serveur
        self.server_socket.close()

        # Redémarrer le script du serveur
        python = sys.executable
        os.execl(python, python, *sys.argv)
    def commande(self):
        serverStatus = 1
        while serverStatus==1:
            commandPrompt = input("root : ")
            if commandPrompt.startswith("/shutdown"):
                self.broadcast("vous allez etre déconnecté dans 1 minute (le serveur va redémarer)", "0.0.0.0")
                time.sleep(10)
                for client_socket, _ in self.clients:
                    try:
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                    except Exception as e:
                        print(f"Erreur lors du shutdown : {e}")


                # Fermer le socket serveur
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
                serverStatus =0
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
                        if client[1][0] == arg2:  # Comparaison avec l'adresse IP
                            # Si l'adresse IP est connectée, déconnecte le client
                            client[0].send("bye".encode('utf-8'))
                            self.remove_client(client[0])
                            print(f"Déconnexion de l'utilisateur avec l'adresse IP {arg2}")
                except IndexError:
                    # Si aucun deuxième argument n'est fourni
                    cursor = self.db_connection.cursor()
                    cursor.execute("INSERT INTO ban(ban) VALUES (%s)", (username,))
                    self.db_connection.commit()
                    cursor.close()
                    print(f"Banning user {username}")
                except Exception as e:
                    print(f"Erreur lors du bannissement : {e}")
                self.restart_server()

            elif commandPrompt.startswith("/send"):
                message=commandPrompt.split()
                message = "serveur > "+' '.join(message[1:])
                self.broadcast(message,"0.0.0.0")


if __name__ == '__main__':
    server = Server()

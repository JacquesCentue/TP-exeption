import socket
import threading
import mysql.connector
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

        # Créer un thread pour écouter les connexions
        threading.Thread(target=self.listen_connections).start()

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
            # Réception du nom d'utilisateur et du mot de passe du client
            username = client_socket.recv(1024).decode('utf-8')
            password = client_socket.recv(1024).decode('utf-8')

            #test de passage des identifiants
            print(username)
            print(f"mot de passe hashé: {password}") # normalement crypté avec pour clé "zabchat" bien sur la clé peut etre autre chose mais identique coté client et serveur
            #password = cryptocode.decrypt(password, "zabchat")
            #print(f"mot de passe décrypté: {password}")
            # Vérification des informations d'authentification dans la base de données
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT user_id,username, rights FROM user WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            #print(user)
            cursor.close()

            if user:
                userid, username, access_rights = user
                # Envoyer l'autorisation au client avec le numéro d'utilisateur et les droits d'accès
                client_socket.send(f"AUTHORIZED,{userid},{username},{access_rights}".encode('utf-8'))
                self.broadcast(f"{username} s'est connecté", "0.0.0.0")



                # Attendre les messages du client
                while True:


                    print(f"userid:{userid}")
                    try:
                        message = client_socket.recv(1024).decode('utf-8')
                        print(message)
                        if message =="bye":
                            self.broadcast(f"{username} s'est déconnecté", "0.0.0.0")

                            self.remove_client(client_socket)


                        if not message:
                            break

                        # Diffusion du message à tous les clients
                        self.broadcast(message, client_address)

                        # Ecriture du message dans le base de donnée pour modération
                        cursor = self.db_connection.cursor()
                        cursor.execute("INSERT INTO generalchat(idsent,message) VALUES (%s,%s)",(userid,message))
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

if __name__ == '__main__':
    server = Server()

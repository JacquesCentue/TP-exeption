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

        self.ipban = []
        self.ipuserban = []



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
            #on raffraichit la liste des utilisateurs et des ip bannies lorsqu'un autre utilisateur se connecte
            self.ipban =[]
            self.userban =[]

            # Reception des paramètres des utilisateurs et ip bannies
            # creation de la liste des ip bannies
            cursor = self.db_connection.cursor(buffered=True)
            cursor.execute("SELECT ipban FROM ban GROUP BY ipban")
            self.ipban = [ip[0] for ip in cursor.fetchall()]
            print(f"adresses IP bannies : {self.ipban}")
            print(f"{self.ipban[0]}")
            for i in range(len(self.ipban)):
                print(f"ip bannie {i} : {self.ipban[i]}")
            cursor.close()

            # creation de la liste des utilisateurs bannis
            cursor = self.db_connection.cursor(buffered=True)
            cursor.execute("SELECT userban FROM ban")
            # Cela permet le formatage de la liste a partir des identifiants, on enleve les parentheses
            self.userban = [user[0] for user in cursor.fetchall()]
            print(f"utilisateurs bannis : {self.userban}")
            for i in range(len(self.userban)):
                print(f"utilisateur banni {i} : {self.userban[i]}")
            print(self.userban)
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



            for i in range(len(self.userban)):
                if username != self.userban[i]:
                    continu=1
                else:
                    client_socket.send("BANNED".encode('utf-8'))

                    # Fermer la connexion du client
                    client_socket.close()

            for i in range(len(self.ipban)):
                if client_address[0] != self.ipban[i] :
                    continu=1
                else:
                    client_socket.send("BANNED".encode('utf-8'))

                    # Fermer la connexion du client
                    client_socket.close()

            if user:
                userid, username, access_rights = user
                # Envoyer l'autorisation au client avec le numéro d'utilisateur et les droits d'accès
                print(f"AUTHORIZED,{userid},{username},{access_rights}")
                client_socket.send(f"AUTHORIZED,{userid},{username},{access_rights}".encode('utf-8'))
                self.broadcast(f"{username} s'est connecté", "0.0.0.0")



                        # Attendre les messages du client
                while True:


                    print(f"userid:{userid}")
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

if __name__ == '__main__':
    server = Server()

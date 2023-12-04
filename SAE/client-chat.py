import socket

host = "localhost" # "", "127.0.0.1
port = 4090

client_socket = socket.socket()
client_socket.connect((host, port))

msg = ""
while msg != "bye":
    msg = input("Message : ")
    if msg != "bye":
        msg = f'{socket.gethostname()}> {msg}'

    client_socket.send(msg.encode())
    print(f"Message envoyé : {msg}")

# Fermeture
client_socket.close()
print("Fermeture de la socket client")

import socket

if __name__ == '__main__':
    host ="10.128.6.12"
    port = 4090
    message = input("votre message : ")
    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_socket.send(message.encode())
    reply ="ok"
    client_socket.recv(1024).decode()
    client_socket.close()
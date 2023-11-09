# -*- coding: latin-1 -*-
import socket


server = socket.socket()


port = 4090
addr_ip = "10.128.6.12"
server.connect((socket.gethostbyaddr(addr_ip)[0], port))

conn=1
while conn==1:

    msg=server.recv(1024)
    print("C>",msg)
    message=input("Message : ")
    server.send(message.encode())
    msgSRV = server.recv(1024)
    print("S>", msgSRV)


conn=0
server.close()
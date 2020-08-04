# source: class book: Computer Networking by Kurose and Ross
import sys
from socket import *

server_port = 4247  # establish port number
server_socket = socket(AF_INET, SOCK_STREAM)  # create streaming socket
server_socket.bind((gethostname(), server_port))  # bind the socket to host and port


def chat():
    counter = 0
    while True:
        data_a = "From server: msg " + str(counter) + "."
        counter = counter + 1
        connection_socket.send(data_a.encode()) # send encoded message
        print(data_a)
        rec_msg = connection_socket.recv(1024).decode()  # receive message
        print(rec_msg)  # print received message
        if rec_msg == "/q":
            connection_socket.close()  # close connection
            server_socket.close()
            sys.exit()
        else:
            continue


# server waits
server_socket.listen(1)
print("The server on port %d is listening." % server_port)
while True:  # connection is established
    connection_socket, address = server_socket.accept()  # accept outside connection
    chat()

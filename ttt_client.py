from socket import *

server_name = gethostname()
port_number = 4246
total_length = 0
# create client socket
# sock_stream indicates TCP socket rather than UDP
client_socket = socket(AF_INET, SOCK_STREAM)
# establish connection between server and client
client_socket.connect((server_name, port_number))
print("Welcome to Tic Tac Toe. To exit, enter /q.")

def empty_board():
    print"Board number key:"
    print("7" + '|' + "8" + '|' + "9")
    print('-+-+-')
    print("4" + '|' + "5" + '|' + "6")
    print('-+-+-')
    print("1" + '|' + "2" + '|' + "3")

def play():
    response = 0
    while True:
        # output message
        rec_msg = client_socket.recv(4026)
        print(rec_msg.decode())
        response = rec_msg[0]
        if response == "#":
            req_msg = raw_input("> ")
            client_socket.send(req_msg.encode())
        else:
            continue


while True:
    play()

client_socket.close()

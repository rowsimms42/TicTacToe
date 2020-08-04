from socket import *

server_name = gethostname()
port_number = 4247
total_length = 0
# create client socket
# sock_stream indicates TCP socket rather than UDP
client_socket = socket(AF_INET, SOCK_STREAM)
# establish connection between server and client
client_socket.connect((server_name, port_number))
print("Welcome. To exit chat, enter /q.")

while True:
    # output message
    rec_msg = client_socket.recv(4026)
    print(rec_msg.decode())
    req_msg = raw_input("> ")
    if req_msg == "/q":
        client_socket.send(req_msg.encode())
        break
    else:
        client_socket.send(req_msg.encode())

client_socket.close()

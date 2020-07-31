# https://medium.com/byte-tales/the-classic-tic-tac-toe-game-in-python-3-1427c68b8874
# https://stackoverflow.com/questions/38412887/how-to-send-a-list-through-tcp-sockets-python/38413006

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

the_board = {'7': ' ', '8': ' ', '9': ' ',
             '4': ' ', '5': ' ', '6': ' ',
             '1': ' ', '2': ' ', '3': ' '}


def print_board(b):
    print(b['7'] + '|' + b['8'] + '|' + b['9'])
    print('-+-+-')
    print(b['4'] + '|' + b['5'] + '|' + b['6'])
    print('-+-+-')
    print(b['1'] + '|' + b['2'] + '|' + b['3'])


def empty_board():
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
            while True:
                req_msg = raw_input("> ")
                if req_msg not in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    print("Number must be between 1 and 9.")
                else:
                    req_msg = req_msg
                    p_num = str(rec_msg[3])
                    if p_num == "1":
                        the_board[req_msg] = 'o'
                    else:
                        the_board[req_msg] = 'x'
                    print_board(the_board)
                    print("")
                    client_socket.send(req_msg.encode())
                    break
        elif response == "|":
            num = str(rec_msg[1])
            if p_n == "o":
                the_board[num] = 'x'
            else:
                the_board[num] = 'o'
            print_board(the_board)
            print("")

        elif response == "*":
            empty_board()
            print("")

        elif response == "@":
            p = str(rec_msg[9])
            if p == "1":
                p_n = "o"
            else:
                p_n = "x"
        else:
            continue


while True:
    play()

client_socket.close()

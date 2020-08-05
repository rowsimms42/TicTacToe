# https://medium.com/byte-tales/the-classic-tic-tac-toe-game-in-python-3-1427c68b8874

import time
from socket import *

server_name = gethostname()
port_number = 4248
total_length = 0
# create client socket
client_socket = socket(AF_INET, SOCK_STREAM)
# establish connection between server and client
client_socket.connect((server_name, port_number))

the_board = {'7': ' ', '8': ' ', '9': ' ',
             '4': ' ', '5': ' ', '6': ' ',
             '1': ' ', '2': ' ', '3': ' '}

#  game board
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
    ex = False
    while True:  # game loop
        rec_msg = client_socket.recv(4026)
        print(rec_msg.decode())
        response = rec_msg[0]

        if response == "#":
            while True:  # input validation
                req_msg = raw_input("> ")
                if req_msg == "/q":
                    ex = True
                    break
                elif req_msg not in {'1', '2', '3', '4', '5', '6', '7', '8', '9'} or the_board[req_msg] != ' ':
                    print("Number must be between 1 and 9 and not already taken.")
                else:
                    req_msg = req_msg
                    the_board[req_msg] = 'x'  # input player move
                    print_board(the_board)
                    print("")
                    break
            if ex:  # exit game
                client_socket.send(req_msg.encode())
                print("Exiting game...")
                break
            else:
                client_socket.send(req_msg.encode())
        elif response == "|":
            num = str(rec_msg[1])
            the_board[num] = 'o'  # input server move
            print_board(the_board)
            print("")
        elif response == "*":  # print empty board at beginning to show key
            empty_board()
            print("")
        elif response == "~":  # game over
            break
        else:
            continue


while True:
    play()
    break
client_socket.close()  # close connection

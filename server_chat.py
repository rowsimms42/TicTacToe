# source: class book: Computer Networking by Kurose and Ross
# https://medium.com/byte-tales/the-classic-tic-tac-toe-game-in-python-3-1427c68b8874

import sys
from socket import *
import random
import time

server_board = {'7': ' ', '8': ' ', '9': ' ',
                '4': ' ', '5': ' ', '6': ' ',
                '1': ' ', '2': ' ', '3': ' '}

move_list = []

server_port = 4248  # establish port number
server_socket = socket(AF_INET, SOCK_STREAM)  # create streaming socket
server_socket.bind(('', server_port))  # bind the socket to host and port


def check_if_won():
    if server_board['7'] == server_board['8'] == server_board['9'] != ' ':
        return True
    elif server_board['4'] == server_board['5'] == server_board['6'] != ' ':
        return True
    elif server_board['1'] == server_board['2'] == server_board['3'] != ' ':
        return True
    elif server_board['1'] == server_board['4'] == server_board['7'] != ' ':
        return True
    elif server_board['2'] == server_board['5'] == server_board['8'] != ' ':
        return True
    elif server_board['3'] == server_board['6'] == server_board['9'] != ' ':
        return True
    elif server_board['7'] == server_board['5'] == server_board['3'] != ' ':
        return True
    elif server_board['1'] == server_board['5'] == server_board['9'] != ' ':
        return True
    else:
        return False


def draw():
    player_socket.send("~~ Draw ~~")


def play():
    counter = 0
    game_over = False
    player_socket.send("Welcome to tic tac toe. To quit during the game, enter /q.")
    time.sleep(1)
    player_socket.send("Server is o. You are x.")
    time.sleep(1)
    player_socket.send("* board key *")
    time.sleep(1)

    while True:  # game loop
        while True:  # validate spot isn't already taken
            r = random.randint(1, 9)
            print("Temp server move: " + str(r))  # output for error checking
            if r not in move_list:
                server_board[str(r)] = 'o'  # add server move
                move_list.append(r)
                break
        print("Server move: " + str(r))
        player_socket.send("|" + str(r) + "| : Servers' move")
        time.sleep(1)
        game_over = check_if_won()
        if game_over:
            player_socket.send("~~ Game over. Server won. ~~")
            break  # exit game loop
        counter += 1
        if counter >= 9:
            draw()
            break  # exit game loop
        player_socket.send("# Enter 1-9")
        rec_msg = player_socket.recv(1024).decode()  # receive message
        if rec_msg == "/q":  # player wants to quit game
            print(rec_msg)
            break
        else:
            move_list.append(int(rec_msg))
            q = str(rec_msg)
            server_board[q] = 'x'
            print("Client move: " + str(q))
            game_over = check_if_won()
            if game_over:
                player_socket.send("~~ Game over. You won. ~~")
                break
            counter += 1
            if counter >= 9:
                draw()
                break


# server waits
server_socket.listen(1)
print("The server on port %d is listening." % server_port)
while True:  # connection is established
    player_socket, address = server_socket.accept()  # accept outside connection
    print("Player has joined game.")
    play()
    print("Exiting game...")
    player_socket.close()  # close client connection
    server_socket.close()  # close server
    sys.exit()  # exit

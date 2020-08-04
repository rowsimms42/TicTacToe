# source: class book: Computer Networking by Kurose and Ross
# https://stackoverflow.com/questions/25005292/multiplayer-snake-game-pythonv
import os
import sys
import thread
import time
from socket import *
from thread import start_new_thread
import multiprocessing
r = True
players = []
game_started = False


server_board = {'7': ' ', '8': ' ', '9': ' ',
                '4': ' ', '5': ' ', '6': ' ',
                '1': ' ', '2': ' ', '3': ' '}

server_port = 4243  # establish port number
server_socket = socket(AF_INET, SOCK_STREAM)  # create streaming socket
server_socket.bind(('', server_port))  # bind the socket to host and port
server_socket.listen(1)
print("The server on port %d is listening." % server_port)


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


def handler(connection_socket, add):
    game_over = False
    ex = False
    time.sleep(1)
    i = 0
    j = 0
    if game_started:
        players[0].send("@ Player 1, you are o.")
        players[1].send("@ Player 2, you are x.")
        time.sleep(1)
        players[0].send("* board key *")
        players[1].send("* board key *")
        time.sleep(1)
        game_loop = True
        while game_loop:
            players[0].send("# P1: Enter 1-9")
            players[1].send("Waiting for your turn...")
            rec_msg_p1 = players[0].recv(1024).decode()  # receive message
            if rec_msg_p1 == "/q":
                players[1].send("~~ A player has exited the game. Goodbye. ~~")
                # players[0].send("~~ A player has exited the game. Goodbye. ~~")
                ex = True
                break
            print(rec_msg_p1)
            p = str(rec_msg_p1)
            server_board[p] = 'o'
            players[1].send("|" + str(rec_msg_p1) + "| : Player 1's move")
            time.sleep(1)
            game_over = check_if_won()
            if game_over:
                players[0].send("~~ Game over. Player 1 won. ~~")
                players[1].send("~~ Game over. Player 1 won. ~~")
                print("Game over. Player 1 won.")
                connection_socket.close()
                ex = True
                break
            players[1].send("# P2: Enter 1-9")
            players[0].send("Waiting for your turn...")
            rec_msg_p2 = players[1].recv(1024).decode()  # receive message
            if rec_msg_p2 == "/q":
                players[0].send("~~ A player has exited the game. Goodbye. ~~")
                # players[0].send("~~ A player has exited the game. Goodbye. ~~")
                ex = True
                break
            q = str(rec_msg_p2)
            server_board[q] = 'x'
            print(rec_msg_p2)
            players[0].send("|" + str(rec_msg_p2) + "| : Player 2's move")
            time.sleep(1)
            game_over = check_if_won()
            if game_over:
                players[0].send("~~ Game over. Player 2 won. ~~")
                players[1].send("~~ Game over. Player 2 won. ~~")
                print("Game over. Player 2 won.")
                connection_socket.close()
                ex = True
                break
        if ex:
            print("Players have left game. Enter control-c to close server.")
            connection_socket.close()
            stop()


def stop():
    conn.close()
    server_socket.close()
    sys.exit()


count = 1
# server waits

while True:  # connection is established
    conn, address = server_socket.accept()  # accept outside connection
    print("Player " + str(count) + " has joined.")
    count += 1
    players.append(conn)
    if len(players) < 2:
        players[0].send("Hello, player 1. Waiting for player 2...")
    if len(players) > 1:
        players[0].send("Player 2 has joined. ")
        players[1].send("Hello, player 2. ")
        game_started = True
    start_new_thread(handler, (conn, address))
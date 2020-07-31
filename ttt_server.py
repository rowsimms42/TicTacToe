# source: class book: Computer Networking by Kurose and Ross
# https://stackoverflow.com/questions/25005292/multiplayer-snake-game-pythonv

import sys
import time
from socket import *
from thread import start_new_thread
import pickle

server_port = 4246  # establish port number
server_socket = socket(AF_INET, SOCK_STREAM)  # create streaming socket
players_temp = []
player_a = []
player_b = []
players = []
c_player = 0
game_started = False

try:
    server_socket.bind((gethostname(), server_port))  # bind the socket to host and port
except socket.error as e:
    str(e)
server_socket.listen(2)
print("The server on port %d is listening." % server_port)


def handler(connection_socket, add):
    p1 = False
    p2 = False
    counter = 0
    length = 0
    a = 0
    b = 0
    time.sleep(1)
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
            rec_msg_p1 = players[0].recv(1024).decode()  # receive message
            print(rec_msg_p1)
            players[1].send("|" + str(rec_msg_p1) + "| : Player 1's move")
            time.sleep(1)
            players[1].send("# P2: Enter 1-9")
            rec_msg_p2 = players[1].recv(1024).decode()  # receive message
            print(rec_msg_p2)
            players[0].send("|" + str(rec_msg_p2) + "| : Player 2's move")
            time.sleep(1)


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

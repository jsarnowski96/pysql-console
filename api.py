# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:00:50 2020

@author: jsarnowski
"""

import socket
import sys
from pysqlconsole import drawInitBoard
from commands import commands
import time
import flask

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1111)
    
def InitServer():
    global server
    server = Server()
    
def EnableServerListeningMode(server):
    server.sock.bind(server.server_address)
    server.sock.listen(1)
    while True:
        connection, client_address = server.sock.accept()
        try:
            print(time.strftime("%c", time.gmtime()) + " - Connection from " + str(client_address))
    
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(4096)
                print("Received data: " + str(data))
                if data:
                    print("Sending back to " + str(client_address) + ".")
                    sock.send(drawInitBoard())
                    connection.sendall(data)
                    #connection.sendall(drawInitBoard())
                else:
                    print("No more data from: " + str(client_address))
                    break
        finally:
            # Clean up the connection
            connection.close()
        
InitServer()
EnableServerListeningMode(server)
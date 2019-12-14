# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:07:47 2019

@author: Jakub Sarnowski
"""

import pyodbc
import sys
from getpass import getpass
import commands as commands

username = None
password = None
success = False


def drawInitBoard():
    print(r"""      
                +-----------------------------------------------------------------------------+
                |                     _..-'(                       )`-.._                     |
                |                  ./'. '||\\.       (\_/)       .//||` .`\.                  |
                |               ./'.|'.'||||\\|..    )O O(    ..|//||||`.`|.`\.               |
                |            ./'..|'.|| |||||\`````` '`"'` ''''''/||||| ||.`|..`\.            |
                |          ./'.||'.|||| ||||||||||||.     .|||||||||||| |||||.`||.`\.         |
                |         /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\         |
                |        '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`        |
                |       '.||| ||||||||| |/'   ``\||``     ''||/''   `\| ||||||||| |||.`       |
                |       |/' \./'     `\./         \!|\   /|!/         \./'     `\./ `\|       |
                |       V    V         V          }' `\ /' `{          V         V    V       |
                |       `    `         `               V               '         '    '       |
                +-----------------------------------------------------------------------------+
                                                                                    
    _/_/_/                _/                    _/_/_/                                          _/           
   _/    _/    _/_/_/  _/_/_/_/              _/          _/_/    _/_/_/      _/_/_/    _/_/    _/    _/_/    
  _/_/_/    _/    _/    _/      _/_/_/_/_/  _/        _/    _/  _/    _/  _/_/      _/    _/  _/  _/_/_/_/   
 _/    _/  _/    _/    _/                  _/        _/    _/  _/    _/      _/_/  _/    _/  _/  _/          
_/_/_/      _/_/_/      _/_/                _/_/_/    _/_/    _/    _/  _/_/_/      _/_/    _/    _/_/_/       
    
                                       +---------------------------------+
                                       |      Welcome to Bat Console     |
                                       |---------------------------------|
                                       |     author: Jakub Sarnowski     |
                                       |     github.com/jsarnowski96     |
                                       +---------------------------------+
    """)
    
def UserAuthentication():    
    global username 
    global password 
    global success   
    try:
        if username != "" or username != None:
            username = None
        if password != "" or password != None:
            password = None
        while username == "" or username == None:
            username = str(input("Username: "))
        while password == "" or password == None:
            password = getpass()
        dbConnection = ""
        if dbConnection:
            dbConnection.close()
        else:
            dbConnection = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                          'Server=localhost;'
                                          'Database=AdventureWorks2012;'
                                          'Trusted_Connection=yes;')    
        cursor = dbConnection.cursor()
        cursor.execute("select username, password from AuthUsers where username = ? and password = ?", username, password)            
        print("+-----------------------------------------------+")
        print("| User Authentication action has been completed |")
        print("+-----------------------------------------------+")
        if cursor.fetchone():
            success = True
            if success is True:        
                print("Welcome back,", username,"\n")
        else:
            print("Authentication failed. Incorrect username or password.\n")
    except pyodbc.Warning as w:
        print(w,": Caution - possible data truncation.")
    except pyodbc.DatabaseError as e:
        print(e,": Could not connect to the database - incorrect server name or database")
    except pyodbc.DataError as e:
        print(e,": Illegal operation detected.")
    except pyodbc.OperationalError as e:
        print(e,": Could not connect to the database server")
    except pyodbc.IntegrityError as e:
        print(e,": Relational integrity of the target database is compromised.")
    except pyodbc.InternalError as e:
        print(e,": Cursor not valid or transaction out of sync")
    except pyodbc.ProgrammingError as e:
        print(e,": Database not found, SQL Syntax error or wrong number of parameters.")
    except pyodbc.NotSupportedError as e:
        print(e,": Database does not support provided pyodbc request.")
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit()
    except SystemExit:
        pass
    except:
        print("UserAuthentication: Unknown error occured during connecting to the database.")

def InputLoop(userInput):
    try:
        if userInput[0] in commands.commands or commands.commands["aliases"].has_key(userInput[0]):
            if userInput[0] == "exit" or userInput == "quit":
                commands.Exit()
                global username
                global password
                username = None
                password = None
                sys.exit()
            if  userInput[0] == "connect":
                try:
                    if userInput[1] and userInput[2]:
                        commands.Connect(srv = userInput[1], db = userInput[2])
                    elif userInput[1]:
                        commands.Connect(srv = userInput[1])
                except IndexError:
                    commands.Connect()
            elif userInput[0] == "close":
                commands.Close()
            elif userInput[0] == "logout":
                commands.Logout()
            elif userInput[0] == "show":
                commands.Show()
            elif userInput[0] == "help":
                commands.Help()
            elif userInput[0] == "export" or userInput[0] == "exp":
                commands.Export()
            elif userInput[0] == "clear" or userInput[0] == "cls":
                commands.Clear()
                drawInitBoard()
                print("\n" * 2)
        else:
            print("Syntax error - " + userInput[0] + " command was not recognized.\n")
    except AttributeError:
        pass
        
# Startup script execution

def MainActivity():
    try:
        userInput = list(map(str,input(username + " $ ").split()))
        InputLoop(userInput)
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit()

try:
    print("\n" * 25)
    drawInitBoard()
    while True:
        if success == False:
            UserAuthentication()
        elif success == True:
            MainActivity()
except KeyboardInterrupt:
    sys.exit()

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:07:47 2019

@author: Jakub Sarnowski
"""

import pyodbc
import sys
from getpass import getpass
import commands as commands
import settings

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
    global success   
    try:
        if settings.global_config_array["username"] != None:
            settings.global_config_array["username"] = None
        if settings.global_config_array["password"] != None:
            settings.global_config_array["password"] = None
            
        username = str(input("Username: "))
        password = getpass()
        settings.global_config_array["username"] = username
        settings.global_config_array["password"] = password
        dbConnection = ""
        
        if settings.global_config_array["secure_sql_user_session"] != None:
            settings.global_config_array["secure_sql_user_session"].close()
            settings.global_config_array["secure_sql_user_session"] = None

        dbConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                          'Server=localhost;'
                                          'Database=master;'
                                          'uid='+username+';'
                                          'pwd='+password+';'
                                          'Trusted_Connection=no;')   
        #cursor = dbConnection.cursor()
        #cursor.execute("select username, password from AuthUsers where username = ? and password = ?", username, password)            
        print("+-----------------------------------------------+")
        print("| User Authentication action has been completed |")
        print("+-----------------------------------------------+")
        #if cursor.fetchone():
        #    success = True
        #    if success is True:        
        #        print("Welcome back,", username,"\n")
        #else:
        #    print("Authentication failed. Incorrect username or password.\n")
        if dbConnection:
            success = True
            settings.global_config_array["secure_sql_user_session"] = dbConnection
            print("Welcome back,", username,"\n")
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
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        print("+-----------------------------------------------+")
        print("| User Authentication action has been completed |")
        print("+-----------------------------------------------+")
        if sqlstate == '28000':
            print("Authentication failed. Incorrect username or password.\n")
        else:
            print("UserAuthentication: Unknown error occured during connecting to the database.\n")

def InputLoop(userInput):
    try:
        if userInput[0] in commands.commands or commands.commands["aliases"].has_key(userInput[0]):
            if userInput[0] == "exit" or userInput == "quit":
                commands.Exit()
                sys.exit()
            if  userInput[0] == "connect":
                try:
                    if userInput[1] and userInput[2]:
                        commands.Connect(server = userInput[1], database = userInput[2])
                    elif userInput[1]:
                        commands.Connect(server = userInput[1])
                except IndexError:
                    commands.Connect()
            elif userInput[0] == "close":
                commands.Close()
            elif userInput[0] == "change":
                commands.Change()
            elif userInput[0] == "logout":
                global success 
                success = False
                commands.Logout()
                drawInitBoard()
            elif userInput[0] == "status":
                commands.Status()
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
    except KeyError:
        print("Syntax error - " + userInput[0] + " command was not recognized.\n")
    except AttributeError:
        print("Syntax error - " + userInput[0] + " command was not recognized.\n")

def MainActivity():
    try:
        userInput = list(map(str,input(settings.global_config_array["username"] + " $ ").split()))
        InputLoop(userInput)
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit()

# Startup execution        
        
try:
    settings.init()
    print("\n" * 25)
    drawInitBoard()
    while True:
        if settings.global_config_array["secure_sql_user_session"] == None and success == False:
            UserAuthentication()
        elif settings.global_config_array["secure_sql_user_session"] and success == True:
            MainActivity()
except KeyboardInterrupt:
    sys.exit()

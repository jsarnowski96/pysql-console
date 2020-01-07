# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:07:47 2019

@author: Jakub Sarnowski
"""

import pyodbc
import sys
from getpass import getpass
import commands as commands
from inspect import signature
import settings

success = False

def drawInitBoard():
    print(r"""      
                         _____   __ __   __  _      ___ __  __  _   __   __  _   ___  
                        | _,\ `v' /' _/ /__\| | __ / _//__\|  \| |/' _/ /__\| | | __| 
                        | v_/`. .'`._`.| \/ | ||__| \_| \/ | | ' |`._`.| \/ | |_| _|  
                        |_|   !_! |___/ \_V_\___|  \__/\__/|_|\__||___/ \__/|___|___| 
                                                                            v.0.2.70

                                     +-----------------------------------+
                                     |      Welcome to PySQL Console     |
                                     |-----------------------------------|
                                     |      author: Jakub Sarnowski      |
                                     |      github.com/jsarnowski96      |
                                     +-----------------------------------+
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
        
        if settings.global_config_array["user_sql_session"] != None:
            settings.global_config_array["user_sql_session"].close()
            settings.global_config_array["user_sql_session"] = None
        dbConnection = pyodbc.connect('Driver={'+settings.global_config_array["driver"]+'};'
                                          'Server=localhost;'
                                          'Database=master;'
                                          'uid='+username+';'
                                          'pwd='+password+';'
                                          'Trusted_Connection=no;')   
        print("+-----------------------------------------------+")
        print("| User Authentication action has been completed |")
        print("+-----------------------------------------------+")
        if dbConnection:
            success = True
            settings.global_config_array["user_sql_session"] = dbConnection
            print("Welcome back,", username,"\n")
    except pyodbc.Warning as w:
        print("Warning:",w.args[0],"\n",w,"\n")
        print("Warning: - possible data truncation.\n")
    except pyodbc.DatabaseError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Could not connect to the database - incorrect server name or database.\n")
    except pyodbc.DataError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Illegal operation detected.\n")
    except pyodbc.OperationalError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Could not connect to the database server.\n")
    except pyodbc.IntegrityError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Relational integrity of the target database is compromised.\n")
    except pyodbc.InternalError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Cursor not valid or transaction out of sync.\n")
    except pyodbc.ProgrammingError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Database not found, SQL Syntax error or wrong number of parameters.\n")
    except pyodbc.NotSupportedError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("Database does not support provided pyodbc request.\n")
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
            print("Error:",e.args[0],"\n",e,"\n")
    except: print("UserAuthentication(): Unknown error occured during connecting to the database.\n")

def InputHandler(userInput):
    try:
        if userInput[0] in commands.commands:
            cmd = userInput[0]
            try:
                userInput.pop(0)
                methodInspect = signature(commands.commands[cmd]["exec"])
                if len(methodInspect.parameters) >= 1:
                    if cmd == "query":
                        userInput = ' '.join(userInput)
                        commands.commands[cmd]["exec"](userInput)
                    else:
                        commands.commands[cmd]["exec"](*userInput)
                else:
                    commands.commands[cmd]["exec"]()
                if cmd == "exit":
                    sys.exit()
                elif cmd == "clear":
                    drawInitBoard()
                    print("\n" * 2)
                elif cmd == "logout":
                    global success
                    success = False
                    drawInitBoard()
            except IndexError:
                commands.commands[cmd]["exec"]()
        elif userInput[0] in commands.commands["aliases"]:
            cmd = userInput[0]
            try:    
                userInput.pop(0)
                methodInspect = signature(commands.commands["aliases"][cmd]["exec"])
                if len(methodInspect.parameters) >= 1:
                    commands.commands["aliases"][cmd]["exec"](*userInput)
                else:
                    commands.commands["aliases"][cmd]["exec"]()
                if cmd == "quit":
                    sys.exit()
                elif cmd == "cls":
                    drawInitBoard()
                    print("\n" * 2)
            except IndexError:
                commands.commands["aliases"][cmd]["exec"]()
        else:
            print("Syntax error - " + userInput[0] + " command was not recognized.\n")
    except KeyError:
        print("Error:",e.args[0],"\n",e,"\n")
    except AttributeError as e:
        print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")

def MainActivity():
    try:
        userInput = list(map(str,input(settings.global_config_array["username"] + " $ ").split()))
        InputHandler(userInput)
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit()

# Startup execution        
def Startup():   
    try:
        settings.init()
        print("\n" * 25)
        drawInitBoard()
        while True:
            if settings.global_config_array["user_sql_session"] == None and success == False:
                UserAuthentication()
            elif settings.global_config_array["user_sql_session"] and success == True:
                MainActivity()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e: print("Error:",e.args[0],"\n",e,"\n")

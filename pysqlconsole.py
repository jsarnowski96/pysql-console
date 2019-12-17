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
                         _____   __ __   __  _      ___ __  __  _   __   __  _   ___  
                        | _,\ `v' /' _/ /__\| | __ / _//__\|  \| |/' _/ /__\| | | __| 
                        | v_/`. .'`._`.| \/ | ||__| \_| \/ | | ' |`._`.| \/ | |_| _|  
                        |_|   !_! |___/ \_V_\___|  \__/\__/|_|\__||___/ \__/|___|___| 
                                                                             v.0.2.0

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
            if userInput[0] == "exit":
                commands.commands[userInput[0]]["exec"]
                sys.exit()
            elif  userInput[0] == "connect":
                try:
                    if userInput[1] and userInput[2]:
                        commands.commands[userInput[0]]["exec"](server = userInput[1], database = userInput[2])
                    elif userInput[1]:
                        commands.commands[userInput[0]]["exec"](server = userInput[1])
                except IndexError:
                    commands.commands[userInput[0]]["exec"]()
            elif userInput[0] == "show":
                try:
                    if userInput[1]:
                        commands.commands[userInput[0]]["exec"](table = userInput[1])
                except IndexError:
                    commands.commands[userInput[0]]["exec"] ()
            elif userInput[0] == "export":
                try:
                    if userInput[1]:
                        commands.commands[userInput[0]]["exec"](table = userInput[1])
                    else:
                        commands.commands[userInput[0]]["exec"]()
                except IndexError:
                    commands.commands[userInput[0]]["exec"]()
            elif userInput[0] == "clear":
                commands.commands[userInput[0]]["exec"]()
                drawInitBoard()
                print("\n" * 2)
            elif userInput[0] == "logout":
                commands.commands[userInput[0]]["exec"]()
                global success
                success = False
                drawInitBoard()
            else:
                commands.commands[userInput[0]]["exec"]()
        elif userInput[0] in commands.commands["aliases"]:
                if userInput[0] == "quit":
                    commands.commands["aliases"][userInput[0]]["exec"]()
                    sys.exit()
                elif userInput[0] == "exp":
                    try:
                        if userInput[1]:
                            commands.commands["aliases"][userInput[0]]["exec"](table = userInput[1])
                        else:
                            commands.commands["aliases"][userINput[0]]["exec"]()
                    except IndexError:
                        commands.commands["aliases"][userInput[0]]["exec"]()
                elif userInput[0] == "cls":
                    commands.commands["aliases"][userInput[0]]["exec"]()
                    drawInitBoard()
                    print("\n" * 2)
                else:
                    commands.commands["aliases"][userInput[0]]["exec"]()
        else:
            print("Syntax error - " + userInput[0] + " command was not recognized.\n")
    except KeyError:
        print("Syntax error - " + userInput[0] + " command was not recognized.\n")
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
Startup()

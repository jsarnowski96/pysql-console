# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:07:47 2019

@author: Jakub Sarnowski
"""

import pyodbc
import sys
from getpass import getpass

username = None
password = None

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
    
    print("\n" * 25)
    drawInitBoard()
    
    username = str(input("Username: "))
    password = getpass()
    dbConnection = ""
    success = False
    
    try:
        if dbConnection:
            pass
        else:
            dbConnection = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                          'Server=localhost;'
                                          'Database=AdventureWorks2012;'
                                          'Trusted_Connection=yes;')    
        #pwdHash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        cursor = dbConnection.cursor()
        cursor.execute("select username, password from AuthUsers where username = ? and password = ?", username, password)            
        print("+-----------------------------------------------+")
        print("| User Authentication action has been completed |")
        print("+-----------------------------------------------+")
        if cursor.fetchone():
            success = True
            if success == True:        
                print("Welcome,", username)
            else:
                print("Authentication failed. Incorrect username or password.")
        else:
            print("Could not connect to the database.")
        dbConnection.close()
        dbConnection = None
    except pyodbc.Warning as w:
        print(w,": Caution - possible data truncation.")
    except pyodbc.DatabaseError as e:
        print(e,": Could not connect to the database - incorrect server name or database")
        UserAuthentication()
    except pyodbc.DataError as e:
        print(e,": Illegal operation detected. Exiting.")
        sys.exit()
    except pyodbc.OperationalError as e:
        print(e,": Could not connect to the database server")
        UserAuthentication()
    except pyodbc.IntegrityError as e:
        print(e,": Relational integrity of the target database is compromised.")
        UserAuthentication()
    except pyodbc.InternalError as e:
        print(e,": Cursor not valid or transaction out of sync")
        UserAuthentication()
    except pyodbc.ProgrammingError as e:
        print(e,": Database not found, SQL Syntax error or wrong number of parameters.")
        UserAuthentication()
    except pyodbc.NotSupportedError as e:
        print(e,": Database does not support provided pyodbc request.")
        UserAuthentication()
    except KeyboardInterrupt:
        print("\nExiting program...")
    except:
        print("Unkown error occured during connecting to the database.")

def InputLoop(userInput):
    global commands
    import commands
    if userInput[0] in commands.commands or userInput in commands.commands["aliases"].keys():
        if userInput[0] == "exit" or userInput == "quit":
            commands.Exit()
        if  userInput[0] == "connect":
            try:
                if userInput[1] and userInput[2]:
                    commands.Connect(userInput[1], userInput[2])
                elif userInput[1]:
                    commands.Connect(userInput[1])
            except IndexError:
                commands.Connect()
        if userInput[0] == "close":
            commands.Close()
        if userInput[0] == "logout":
            commands.Logout()
            UserAuthentication()
        if userInput[0] == "show":
            commands.Show()
        if userInput[0] == "export" or userInput[0] == "exp":
            commands.Export()
        if userInput[0] == "clear" or userInput[0] == "cls":
            commands.Clear()
            drawInitBoard()
            print("\n" * 2)
    else:
        print("Syntax error - " + userInput + " command was not recognized.")
        
# Startup script execution

def MainActivity():  
    global username
    
    while True:
        userInput = list(map(str,input(username + " $ ").split()))
        InputLoop(userInput)
try:    
    UserAuthentication()
    MainActivity()
except SystemExit:
    print("\nExiting program...")
except KeyboardInterrupt:
    print("\nExiting program...")
except:
    print("\nUnknown error occured.")
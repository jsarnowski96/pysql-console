# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 18:07:47 2019

@author: Jakub Sarnowski
"""

import pyodbc
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
    """)
    
    print("\t\t\t +----------------------------+")
    print("\t\t\t |      Welcome to BatCon     |")
    print("\t\t\t |----------------------------|")
    print("\t\t\t |   author: Jakub Sarnowski  |")
    print("\t\t\t |   github.com/jsarnowski96  |")
    print("\t\t\t +----------------------------+")
    
def UserAuthentication():
    global username 
    global password 
    
    print("\n" * 50)
    drawInitBoard()
    print("\n" * 5)
    
    username = str(input("Username: "))
    password = getpass()
    dbConnection = ""
    success = False
    
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
        print("Welcome,", username)
        success = True
    else:
        print("Authentication failed. Incorrect username or password.")
        UserAuthentication()
    dbConnection.close()
    dbConnection = None
    print()
    if success == True:        
        MainActivity()

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
    else:
        print("Syntax error - " + userInput + " command was not recognized.")
        
# Startup script execution

def MainActivity():  
    global username
    
    while True:
        userInput = list(map(str,input(username + " $ ").split()))
        InputLoop(userInput)
    
UserAuthentication()    
raise SystemExit
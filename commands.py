# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc
import sys
import main

commands = {
    "exit": "Exit the program",
    "connect": "Make a connection to the target database",
    "close": "Close active connection to the database",
    "logout": "Return to splash screen",
    "show": "List all rows in the selected table",
    "add": "Add new record to the selected table",
    "delete": "Remove the existing record from the selected table",
    "edit": "Modify the existing record in the selected table",
    "help": "Displays all available commands",
    "export": "Exports currently selected table to .csv file",
    "clear": "This command clears the console window",
    "aliases": {
        "cls": "This command clears the console window",
        "exp": "Exports currently selected table to .csv file",
        "quit": "Exit the program",
        "del": "Remove the existing record from the selected table"
    }
}

dbConnection = ""
database = ""
server = ""
table = ""
result = ""

def Exit():
    global dbConnection
    global database
    global server
    global table
    
    main.username = None
    main.password = None
    if dbConnection:
        dbConnection.close()
    dbConnection = None
    server = None
    database = None
    table = None

    sys.exit()

def Connect(srv = "", db = ""):
   # import main
    
    #kwargs = {}
    #if srv != "":
   #     kwargs[main.userInput[1]] = srv
  #  if db != "":
     #   kwargs[main.userINput[2]] = db
        
    
    try:
        global dbConnection
        global server
        global database
        
        if dbConnection == "":
            if srv == "":
                srv = str(input("Server name: "))
                server = srv
            else:
                server = srv    
            if db == "":
                db = str(input("Database: "))
                database = db
            else:
                database = db
            
            if server:
                if database:
                    dbConnection = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                              'Server='+server+';'
                                              'Database='+database+';'
                                              'Trusted_Connection=yes;')
                    print("Successfully connected to the ",server,"->",database)
                else:
                    print("You did not enter database name.")
            else:
                print("You did not enter server name.")
        else:
            print("Connection is already establised.")
    except pyodbc.Warning:
        print("Warning: Caution - possible data truncation.")
    except pyodbc.DatabaseError:
        print("DatabaseError: Could not connect to the database - incorrect server name or database")
    except pyodbc.DataError:
        print("DataError: Illegal operation detected. Exiting.")
    except pyodbc.OperationalError:
        print("OperationalError: Could not connect to the database server")
    except pyodbc.IntegrityError:
        print("IntegrityError: Relational integrity of the target database is compromised.")
    except pyodbc.InternalError:
        print("InternalError: Cursor not valid or transaction out of sync")
    except pyodbc.ProgrammingError:
        print("ProgrammingError: Database not found, SQL Syntax error or wrong number of parameters.")
    except pyodbc.NotSupportedError:
        print("NotSupportedError: Database does not support provided pyodbc request.")
    except KeyboardInterrupt:
        print("\nExiting program...")
    except:
        print("Connect: Unkown error occured during connecting to the database.")
    return


def Close():
    global dbConnection
    if dbConnection:
        dbConnection.close()
    else:
        print("There is no active connection to any database\n")
    return
        
def Logout():
    import main
    main.username = None
    main.password = None
    Clear()
    return
        
def Show(tbl = ""):
    global dbConnection
    global database
    global table
    global result
    
    if dbConnection:
        if tbl == "":
            tbl = str(input("Table name: "))
        table = tbl
        
        if table != "" and table:
            queryAppend = list("select * from ")
            for t in table:
                queryAppend.append(t)
            query = ''.join(queryAppend)
            cursor = dbConnection.cursor()
            result = cursor.execute(query)
            #print(str(result.count()) + " records detected")
            print("Contents of table " + table + ":")
            for i in result.description:
                print(i[0] + "\t")
            print()
            i = 0
            row = result.fetchall()
            for r in row:
                if i <= len(row):
                    print(str(i), r, "\t")
                    i += 1
        else:
            print("You did not enter table's name.\n")
    else:
        print("There is no active connection to the database.\n")
    return
            
def Export(tbl = ""):
    global table
    global dbConnection
    if dbConnection != "" or dbConnection:
        if tbl == "":
            if table == "":
                tbl = str(input("Table name: "))
            if table != "" or table:
                fileBase = table
                fileName = fileBase + ".csv"
                queryAppend = list("select * from ")
                for t in table:
                    queryAppend.append(t)
                query = ''.join(queryAppend)
                cursor = dbConnection.cursor()
                result = cursor.execute(query)
                with open(fileName, "a+", newline='') as csvfile:
                    import csv
                    writer = csv.writer(csvfile)
                    writer.writerow([x[0] for x in result.description])  # column headers
                    row = result.fetchall()
                    for r in row:
                        writer.writerow(row)
            else:
                print("You did not select any source table.\n")
    else:
        print("There is no connection established.\n")
    return
        
def Clear():
    print("\n" * 50)
    return
    
def Help():
    print("\nList of available commands:")
    for k, v in commands.items():
        if k != "aliases":
            print(k,":", v)
    print("\nList of aliases:")
    for k, v in commands["aliases"].items():
        print(k,":", v)
    return
        

            

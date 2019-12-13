# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc

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
    
    global main
    import main
    
    if main.username != "":
        main.username = None
    if main.password != "":
        main.password = None    
    if dbConnection != "":
        if dbConnection:
            dbConnection.close()
            dbConnection = None
        else:
            dbConnection = None
    if database != "":
        database = None
    if server != "":
        server = None
    if table != "":
        table = None
    exit(0)

def Connect(srv = "", db = ""):
    global dbConnection
    global server
    global database
   # import main
    
    #kwargs = {}
    #if srv != "":
   #     kwargs[main.userInput[1]] = srv
  #  if db != "":
     #   kwargs[main.userINput[2]] = db
        
    
    try:
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
    except pyodbc.Warning as w:
        print(w,": Caution - possible data truncation.")
    except pyodbc.DatabaseError as e:
        print(e,": Could not connect to the database - incorrect server name or database")
    except pyodbc.DataError as e:
        print(e,": Illegal operation detected. Exiting.")
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
    except:
        print("Unkown error occured during connecting to the database.")


def Close():
    global dbConnection
    if dbConnection:
        dbConnection.close()
    else:
        print("You have no active connection to any database")
        
def Logout():
    import main
    main.username = None
    main.password = None
    Clear()
        
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
            print("You did not enter table's name.")
    else:
        print("There is no active connection to the database.")
            
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
                print("You did not select any source table.")
    else:
        print("There is no connection established.")
        
def Clear():
    import main
    print("\n" * 50)
    main.drawInitBoard()
    print("\n" * 2)

            

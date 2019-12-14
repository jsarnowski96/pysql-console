# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc
import settings

commands = {
    "exit": "Exit the program" ,
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

def Exit():
    if settings.global_config_array["server"] != None:
        settings.global_config_array["server"] = None
    if settings.global_config_array["database"] != None:
        settings.global_config_array["database"] = None
    if settings.global_config_array["table"] != None:
        settings.global_config_array["table"] = None
    if settings.global_config_array["active_sql_connection"] != None:
        if settings.global_config_array["active_sql_connection"]:
            settings.global_config_array["active_sql_connection"].close()
            settings.global_config_array["active_sql_connection"] = None

def Connect(server = "", database = ""):
    try:                
        username = settings.global_config_array["username"]
        password = settings.global_config_array["password"]
        
        if settings.global_config_array["active_sql_connection"] == None:
            dbConnection = None
            if dbConnection == None:
                if server == "":
                    server = str(input("Server name: "))
                if database == "":
                    database = str(input("Database: "))
    
                settings.global_config_array["server"] = server
                settings.global_config_array["database"] = database
                            
                if server:
                    if database:
                        dbConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                              'Server='+server+';'
                                              'Database='+database+';'
                                              'uid='+username+';'
                                              'pwd='+password+';'
                                              'Trusted_Connection=no;') 
                        print("Successfully connected to the %s->%s.\n" % (server, database))
                    else:
                        print("You did not enter database name.")
                else:
                    print("You did not enter server name.")
            settings.global_config_array["active_sql_connection"] = dbConnection
        elif settings.global_config_array["active_sql_connection"]:
            print("Connection is already established.\n")
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
        dbConnection.close()
        print("\nTerminating command...\n")
    except:
        print("Connect: Unknown error occured during connecting to the database.")

def Close():
    if settings.global_config_array["table"] != None:
        settings.global_config_array["table"] = None
    if settings.global_config_array["active_sql_connection"] != None:
        if settings.global_config_array["active_sql_connection"]:
            settings.global_config_array["active_sql_connection"].close()
            settings.global_config_array["active_sql_connection"] = None
            print("Connection to %s->%s closed.\n" % (settings.global_config_array["server"], settings.global_config_array["database"]))
        if settings.global_config_array["server"] != None:
            settings.global_config_array["server"] = None
        if settings.global_config_array["database"] != None:
            settings.global_config_array["database"] = None
    else:
        print("There is no active connection to any database\n")
        
def Logout():
    if settings.global_config_array["secure_sql_user_session"] != None:
        if settings.global_config_array["secure_sql_user_session"]:
            settings.global_config_array["secure_sql_user_session"].close()
            settings.global_config_array["secure_sql_user_session"] = None
    if settings.global_config_array["username"] != None:
        settings.global_config_array["username"] = None
    if settings.global_config_array["password"] != None:
        settings.global_config_array["password"] = None
    print("\nUser logged out...\n")
        
def Show(table = ""):
    result = ""
    
    try:
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if table == "":
                table = str(input("Table name: "))                
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
            queryAppend = list("select * from ")
            for t in table:
                queryAppend.append(t)
            query = ''.join(queryAppend)
            cursor = dbConnection.cursor()
            result = cursor.execute(query)
            #print(str(result.count()) + " records detected")
            columns = [column[0] for column in result.description]
            print("\nContents of table " + table + ":")
            print("-" * sum(len(i) for i in columns) * 2)
            for i, c in enumerate(columns):
                if i == 0 :
                    print(c,"\t|\t", end = '')
                elif i == len(columns) - 1:
                    print(c,"\t|")
                else:
                    print(c,"\t|\t", end = '')
            print("-" * sum(len(i) for i in columns) * 2)
            rows = result.fetchall()
            for row in rows:
                print("-" * 100)
                print(row)
                print("-" * 100)
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("\nTerminating command...\n")
            
def Export(table = ""):
    try:
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if table == "":
                table = str(input("Table name: "))
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
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
            print("There is no connection established. Redirecting to connect action...\n")
            Connect()
    except KeyboardInterrupt:
        print("\nTerminating command...\n")
        
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

if KeyboardInterrupt:
    print("\nTerminating command...\n")
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc
import os
import settings

path = os.getcwd()

commands = {
    "exit": "Exit the program" ,
    "connect": "Open new connection to the target database",
    "close": "Close active connection to the database",
    "logout": "Return to splash screen",
    "show": "List all rows in the selected table",
    "add": "Add new record to the selected table",
    "delete": "Remove the existing record from the selected table",
    "edit": "Modify the existing record in the selected table",
    "switch": "Modify the current table's focus. If no new table name is provided, it removes focus entirely. Otherwise the focus is placed on the another table.",
    "help": "Displays all available commands",
    "export": "Exports currently selected table to .csv file",
    "clear": "This command clears the console window",
    "status": "Displays current session's data",
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
                                              'Trusted_Connection=no;', timeout = 1) 
                        print("Successfully connected to the %s->%s.\n" % (server, database))
                    else:
                        print("You did not enter database name.")
                else:
                    print("You did not enter server name.")
            settings.global_config_array["active_sql_connection"] = dbConnection
        elif settings.global_config_array["active_sql_connection"]:
            print("Connection is already established.\n")
    except pyodbc.Warning as w:
        print("Warning:",w.args[0],"\n",w,"\n")
        print("Warning: possible data truncation.\n")
    except pyodbc.DatabaseError as e:
        sqlstate = e.args[0]
        if sqlstate == '08001':
            print("Error:",e.args[0],"Connection timeout - could not connect to the SQL server.\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except pyodbc.DataError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("DataError: Illegal operation detected. Exiting.\n")
    except pyodbc.OperationalError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("OperationalError: Could not connect to the database server.\n")
    except pyodbc.IntegrityError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("IntegrityError: Relational integrity of the target database is compromised.\n")
    except pyodbc.InternalError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("InternalError: Cursor not valid or transaction out of sync\n")
    except pyodbc.ProgrammingError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("ProgrammingError: Database not found, SQL Syntax error or wrong number of parameters.\n")
    except pyodbc.NotSupportedError as e:
        print("Error:",e.args[0],"\n",e,"\n")
        print("NotSupportedError: Database does not support provided pyodbc request.\n")
    except KeyboardInterrupt:
        dbConnection.close()
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '28000':
            print("Database",database,"not found.\n")
        else: print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")
    except:
        print("Connect: Unknown error occured during connecting to the database.\n")

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
    print("User logged out...\n")
    Clear()
        
def Show(table = ""):
    try:
        result = ""
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
            if table == "":
                    table = str(input("Table name: "))
            queryAppend = list("select * from ")
            for t in table:
                queryAppend.append(t)
            query = ''.join(queryAppend)
            cursor = dbConnection.cursor()
            result = cursor.execute(query)
            dbConnection.add_output_converter(-155, handle_datetimeoffset)
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
            print()
            settings.global_config_array["table"] = table
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Table",table," does not exist in the",settings.global_config_array["database"],"database.\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")
            
def Export(table = ""):
    try:
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            exportPath = settings.global_config_array["exportPath"]
            if os.path.exists(exportPath):
                pass
            else:
                os.mkdir(exportPath)
                print("Creating /exports directory.\n")
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
            if table == "":
                table = str(input("Table name: "))    
            fileName = table + ".csv"
            queryAppend = list("select * from ")
            for t in table:
                queryAppend.append(t)
            query = ''.join(queryAppend)
            cursor = dbConnection.cursor()
            result = cursor.execute(query)
            finalPath = os.path.join(path, exportPath, fileName)
            if os.path.exists(finalPath):
                print("File",fileName,"already exists. Do you want to overwrite it? [Y/n]", end='')
                confirmAction = str(input())
                if confirmAction == "Y" or confirmAction == "y":
                    with open(finalPath, "a+", newline='') as csvfile:
                        import csv
                        csvfile.truncate(0)
                        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([x[0] for x in result.description])  # column headers
                        rows = result.fetchall()
                        for row in rows:
                            writer.writerow(row)
                        csvfile.close()
                        print("Export of file",fileName,"finished successfully.\n")
                elif confirmAction == "N" or confirmAction == "n":
                    print("Aborting...\n")
            else:
                with open(finalPath, "a+", newline='') as csvfile:
                    import csv
                    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([x[0] for x in result.description])  # column headers
                    rows = result.fetchall()
                    for row in rows:
                        writer.writerow(row)
                csvfile.close()
                print(fileName,"export task finished successfully.\n")
        else:
            print("There is no connection established. Redirecting to connect action...\n")
            Connect()
    except KeyboardInterrupt:
        print("\nTerminating command...\n")
    except AttributeError as e:
        print("Error:",e.args[0],"\n",e,"\n")
    except pyodbc.DataError as e:
        sqlstate = e.args[0]
        if sqlstate == 'HY106':
            print("Conversion error occured - not supported data type field detected. Cannot display content of the table",table,"\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '42S02':
            print("Table",table,"not found.\n")
        else: print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")
    except: print("Could not save file",fileName,"to specified location.\n")
        
def Clear():
    print("\n" * 50)
    return
    
def Help():
    print("\nList of available commands:")
    print("---------------------------")
    for k, v in commands.items():
        if k != "aliases":
            print(k,":", v)
    print("\nList of aliases:")
    print("----------------")
    for k, v in commands["aliases"].items():
        print(k,":", v)
        
def Status():
    i = 0
    print("+" + "-" * 100 + "+")
    for k, v in settings.global_config_array.items():
        if v != None and i < len(settings.global_config_array) - 2:
            print("|",k,"\t\t\t|",v,"\t\t\t\t\t\t\t     |")
        elif v == None and i < len(settings.global_config_array) - 2:
            print("|",k,"\t\t\t|",v,"\t\t\t\t\t\t\t\t     |")
        if k == "secure_sql_user_session" or k == "active_sql_connection":
            if v == None:
                print("|",k,"\t|",v,"\t\t\t\t\t\t\t\t     |")
            else:
                print("|",k,"\t|",v,"\t\t     |")
        if i < len(settings.global_config_array) - 1:
            print("|" + "-" * 100 + "|")
        i += 1
    print("+" + "-" * 100 + "+\n")
    
def Switch(table = ""):
    if table == "":
        print("Removed focus from the",settings.global_config_array["table"],"table.\n")
    if settings.global_config_array["table"] != None:
        settings.global_config_array["table"] = None
    if table != "":
        settings.global_config_array["table"] = table
        

def Add():
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            if settings.global_config_array["table"] != None:
                pass
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '42S02':
            print("No active connection to the database detected. Redirecting to connect action...\n")
            Connect()
        else:
            print("Error:",e.args[0],"\n",e)
    except Exception as e:
        print("Error:",e.args[0],"\n",e)
            
def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

if KeyboardInterrupt:
    print("\nTerminating command...\n")

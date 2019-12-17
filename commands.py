# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc
import os
from tabulate import tabulate
import settings

path = os.getcwd()

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
                if server == "" and database == "":
                    server = str(input("Server name: "))
                    if server == "":
                        print("You did not enter server name.\n")
                    database = str(input("Database name: "))
                    if database == "":
                        print("You did not enter database name.\n")
                    if server != "" and database != "":
                        settings.global_config_array["server"] = server
                        settings.global_config_array["database"] = database
                        dbConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                                     'Server='+server+';'
                                                     'Database='+database+';'
                                                     'uid='+username+';'
                                                     'pwd='+password+';'
                                                     'Trusted_Connection=no;', timeout = 1) 
                        print("Successfully connected to the %s->%s.\n" % (server, database))
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
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
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
    global success
    for k, v in settings.global_config_array.items():
        settings.global_config_array[k] = None
    print("User logged out...\n")
    Clear()
        
def Show(table = ""):
    try:
        result = ""
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None and table == "":
                table = settings.global_config_array["table"]
            elif settings.global_config_array["table"] != None and table != "":
                pass
            elif settings.global_config_array["table"] == None and table == "":
                table = str(input("Table name: "))
            elif settings.global_config_array["table"] == None and table != "":
                pass
            queryAppend = list("select * from ")
            for t in table:
                queryAppend.append(t)
            query = ''.join(queryAppend)
            cursor = dbConnection.cursor()
            result = cursor.execute(query)
            #dbConnection.add_output_converter(-155, handle_datetimeoffset)
            columns = [column[0] for column in result.description]
            headers = []
            for c in columns:
                headers.append(c)
            rows = result.fetchall()
            content = []
            for row in rows:
                r = None
                content.append(row)
            print(tabulate(content, headers, tablefmt="psql"),"\n")
            settings.global_config_array["table"] = table
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
            if table != "":
                Show(table)
            else:
                Show()
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
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
                if table == "":
                    table = settings.global_config_array["table"]
                else: pass
            else:
                if table == "":
                    table = str(input("Table name: "))
                else: pass
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
            if table != "":
                Export(table)
            else:
                Export()
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
    except AttributeError as e:
        print("Error:",e.args[0],"\n",e,"\n")
    except pyodbc.DataError as e:
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
    
def Help():
    print("\nList of available commands:")
    print("---------------------------")
    for k, v in commands.items():
        if k != "aliases":
            print(k,":", v["descr"])
    print("\nList of aliases:")
    print("----------------")
    for k, v in commands["aliases"].items():
        print(k,":", v["descr"])
        
def Status():
    table = []
    for k, v in settings.global_config_array.items():
        table.append([k, v])
    print(tabulate(table, tablefmt="psql"),"\n")
    
def Switch(table = ""):
    if table == "":
        print("Removed focus from the",settings.global_config_array["table"],"table.\n")
    if settings.global_config_array["table"] != None:
        settings.global_config_array["table"] = None
    if table != "":
        settings.global_config_array["table"] = table
        print("Switched focus to table " + table + ".\n")
        
def Add():
    '''
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
            else:
                table = str(input("Please insert the table's name: "))
            cursor = dbConnection.cursor()
            #column_data = cursor.columns(table=settings.global_config_array["table"], catalog=settings.global_config_array["database"], schema='dbo').fetchall()
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = " + "'"+ table + "'").fetchall()
            columns = [c for c in cursor.fetchall()]
            query = list("insert into " + table + "(")
            query.extend(str(columns))
            query.append(") values(")
            values = []
            for i, col in enumerate(columns):
                if i < len(columns) - 1:
                    query.append("?, ")
                else:
                    query.append("?)")
                values.append(input(str(col[0]) + ":"))                    
            finalQuery = ''.join(query)
            insert = cursor.execute(finalQuery, values)
            dbConnection.commit()
            dbConnection.close()
            print("New row has been added to table " + table + ".\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
            Add()
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '42S02':
            print("There is no active connection to the database detected. Redirecting to connect action...\n")
            Connect()
        else:
            print("Error:",e.args[0],"\n",e)
    except Exception as e:
        print("Error:",e.args[0],"\n",e)
    '''
    pass

def Delete(table = "", quantity = 1):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None and table == "":
                table = settings.global_config_array["table"]
            elif settings.global_config_array["table"] == None and table != "":
                pass
            elif settings.global_config_array["table"] != None and table != "":
                pass
            elif settings.global_config_array["table"] == None and table == "":
                table = str(input("Please insert the table's name: "))
            for i in range(quantity):
                recordId = int(input("Record ID: "))
                cursor = dbConnection.cursor()
                queryAppend = list("delete from " + table + " where id = ?")
                query = ''.join(queryAppend)
                print("Are you sure you want to delete the following record? [Y/n]: ", end='')
                confirmation = str(input())
                if confirmation == 'Y' or confirmation == 'y':
                    delete = cursor.execute(query, str(recordId))
                    dbConnection.commit()
                    print("Record ID " + str(recordId) + " removed from the table " + table + ".\n")
                elif confirmation == "N" or confirmation == "n":
                    dbConnection.rollback()
                    print("Transaction cancelled.\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
            if table == "":
                Delete()
            else:
                Delete(table)
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '42S02':
            print("There is no active connection to the database detected. Redirecting to connect action...\n")
            Connect()
        else:
            print("Error:",e.args[0],"\n",e)
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e)

def Edit():
    pass

def Query():
    try:
        if settings.global_config_array["active_sql_connection"]:
            dbConnection = settings.global_config_array["active_sql_connection"]
            print("Insert your query statement:")
            query = str(input())
            result = ""
            if "select" in query:
                cursor = dbConnection.cursor()
                result = cursor.execute(query)
                #dbConnection.add_output_converter(-155, handle_datetimeoffset)
                columns = [column[0] for column in result.description]
                headers = []
                for c in columns:
                    headers.append(c)
                rows = result.fetchall()
                content = []
                for row in rows:
                    r = None
                    content.append(row)
                print(tabulate(content, headers, tablefmt="psql"),"\n")
            else:
                print("Notification: query command allows only for select statements. Use add, delete or edit command for other CRUD operations.\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()      
            Query()                  
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Table",table," does not exist in the",settings.global_config_array["database"],"database.\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")
def List(database = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            if database == "":
                database = settings.global_config_array["database"]
            elif database != "":
                pass
            dbConnection = settings.global_config_array["active_sql_connection"]
            cursor = dbConnection.cursor()    
            query = list("select table_name from " + database + ".information_schema.tables")
            finalQuery = ''.join(query)
            result = cursor.execute(finalQuery)
            rows = result.fetchall()
            table = []
            for row in rows:
                table.append(row)
            print("List of tables in the database " + database)
            print(tabulate(table, headers=["Table name"], tablefmt="psql"), "\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            Connect()
            List(database)
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        print("Terminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Table",table," does not exist in the",settings.global_config_array["database"],"database.\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")    
    

def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

commands = {
    "exit": { "exec": Exit, "descr": "Exit the program" },
    "connect": { "exec": Connect, "descr": "Open new connection to the target database" },
    "close": { "exec": Close, "descr": "Close active connection to the database" },
    "logout": { "exec": Logout, "descr": "Return to splash screen" },
    "show": { "exec": Show, "descr": "List all rows in the selected table" },
    "add": { "exec": Add, "descr": "Add new record to the selected table" },
    "delete": { "exec": Delete, "descr": "Remove the existing record from the selected table" },
    "edit": { "exec": Edit, "descr": "Modify the existing record in the selected table" },
    "list": { "exec": List, "descr": "Display list of tables in the selected database" },
    "switch": { "exec": Switch, "descr": "If no new table name is provided, remove focus from the current table, otherwise switch to the another table." },
    "help": { "exec": Help, "descr": "Displays all available commands" },
    "export": { "exec": Export, "descr": "Exports currently selected table to .csv file" },
    "clear": { "exec": Clear, "descr": "This command clears the console window" },
    "status": { "exec": Status, "descr": "Displays current session's data" },
    "query": { "exec": Query, "descr": "Run a specific query in the database" },
    "aliases": {
        "cls": { "exec": Clear, "descr": "This command clears the console window" },
        "exp": { "exec": Export, "descr": "Exports currently selected table to .csv file" },
        "quit": { "exec": Exit, "descr": "Exit the program" },
        "del": { "exec": Delete, "descr": "Remove the existing record from the selected table" }
    }
}
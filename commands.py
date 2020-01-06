# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:11:41 2019

@author: Jakub Sarnowski
"""

import pyodbc
import os
import datetime
import csv
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
                try:
                    while server == "":
                        server = str(input("Server name: "))
                        if server == "":
                            print("You did not enter server name.\n")
                except KeyboardInterrupt:
                    print("\nTerminating command...\n")
                try:
                    while database == "":
                        database = str(input("Database name: "))
                        if database == "":
                            print("You did not enter database name.\n")
                except KeyboardInterrupt:
                    print("\nTerminating command...\n")
                if server != "" and database != "":
                    settings.global_config_array["server"] = server
                    settings.global_config_array["database"] = database
                    dbConnection = pyodbc.connect('Driver={'+settings.global_config_array["driver"]+'};'
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
        dbConnection = None
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
    global success
    for k, v in settings.global_config_array.items():
        if k != "driver" and k != "exportPath":
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
            if settings.global_config_array["table"] == None and table == "":
                while table == "":
                    table = str(input("Table name: "))
                    if table == "":
                        print("You did not enter table name.\n")
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
            try:
                Connect()
                if table != "":
                    Show(table)
                else:
                    Show()
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Table",table,"does not exist in the",settings.global_config_array["database"],"database.\n")
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
            if settings.global_config_array["table"] != None and table == "":
                table = settings.global_config_array["table"]
            elif settings.global_config_array["table"] == None and table == "":
                while table == "":    
                    table = str(input("Table name: "))
                    if table == "":
                        print("You did not enter table name.\n")
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
                        print(fileName,"has been created.\nExport task finished successfully.\n")
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
                print(fileName,"has been created.\nExport task finished successfully.\n")
        else:
            print("There is no connection established. Redirecting to connect action...\n")
            try:
                Connect()
                if table != "":
                    Export(table)
                else:
                    Export()
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
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
    for k, v in sorted(commands.items()):
        if k != "aliases":
            print(k,":", v["descr"])
    print("\nList of aliases:")
    print("----------------")
    for k, v in sorted(commands["aliases"].items()):
        print(k,":", v["descr"])
    print()
        
def Status():
    table = []
    for k, v in settings.global_config_array.items():
        table.append([k, v])
    print(tabulate(table, tablefmt="psql"),"\n")
    
def Switch(table = ""):
    if table == "":
        print("Removed focus from the",settings.global_config_array["table"],"table.\n")
    if settings.global_config_array["table"] != None:
        if table != "":
            settings.global_config_array["table"] = table
            print("Switched focus to table " + table + ".\n")
        else:
            print("Removed focus from table " + settings.global_config_array["table"])
            settings.global_config_array["table"] = None
        
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

def Delete(table = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None and table == "":
                table = settings.global_config_array["table"]
            elif settings.global_config_array["table"] == None and table == "":
                while table == "":
                    table = str(input("Please insert the table's name: "))
                    if table == "":
                        print("You did not enter table name.\n")
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
            try:
                Connect()
                if table == "":
                    Delete()
                else:
                    Delete(table)
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
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
        dbConnection = None
        print("\nTerminating command...\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e)

def Edit(table = "", recordId = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            dbConnection = settings.global_config_array["active_sql_connection"]
            if settings.global_config_array["table"] != None:
                table = settings.global_config_array["table"]
            else:
                while table == "":
                    table = str(input("Please insert the table's name: "))
                    if table == "":
                        print("You did not enter table name.\n")
            print("Target table's content:\n")
            Show(table)
            while recordId == "":
                recordId = str(input("Please insert record ID: "))
                if recordId == "":
                    print("You did not enter record ID.\n")
            cursor = dbConnection.cursor()
            ListColumnNames = list("select column_name from information_schema.columns where table_name = '" + table + "'")
            ListColumnNamesQuery = ''.join(ListColumnNames)           
            getColumnNames = cursor.execute(ListColumnNamesQuery).fetchall()
            columns = list(str(g) for g in getColumnNames)
            columns = list([c.replace('(','').replace(')','').replace(' ','').replace("'",'').replace(',','').strip() for c in columns])
            getRowIdValues = list("select * from " + table + " where id = " + recordId)
            getRowIdValuesQuery = ''.join(getRowIdValues)
            rowValues = cursor.execute(getRowIdValuesQuery).fetchone()
            rowValuesList = list(str(row) for row in rowValues)
            values = []
            updateQuery = "update " + table + " set ({0}) = ({1})"
            for i in range(1, len(columns) - 1):
                if i < len(columns) - 1:
                    value = (str(input("(" + str(columns[i]) + ")(Current value: '" + str(rowValuesList[i]) + "'): ")))
                    if value == "":
                        continue
                    else:
                        values.append(str(value))                        
                        updateQuery = updateQuery.format(','.join(columns[i]).join('?'))
            updateQuery = updateQuery.join(" where id = " + str(recordId))
            cursor.execute(updateQuery, values)
            dbConnection.commit()
            print("Row ID " + recordId + " in table " + table + " has been updated.\n")
        else:
            print("There is no active connection to the database detected. Redirecting to connect action...\n")
            try:
                Connect()
                if table != "" and recordId != "":
                    Edit(table, recordId)
                elif table != "" and recordId == "":
                    Edit(table)
                elif table == "" and recordId == "":
                    Edit()
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '42S02':
            print("Error" + e.args[0] + ": Table " + table + " does not exist.\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")
        #DEBUG
        print(updateQuery)
        for v in values:
            print(v, end='\t')
        print()
        for c in columns:
            print(c, end='\t')
        print()
        #DEBUG

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
            try:
                Connect()      
                Query()                  
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
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
            if settings.global_config_array["database"] != None:
                if database == "":
                    database = settings.global_config_array["database"]
            else:
                while database == "":
                    database = str(input("Enter database name: "))
                    if database == "":
                        print("You did not enter database name.\n")
            dbConnection = settings.global_config_array["active_sql_connection"]
            cursor = dbConnection.cursor()    
            query = list("select table_schema, table_name from " + database + ".information_schema.tables order by table_schema, table_name")
            finalQuery = ''.join(query)
            result = cursor.execute(finalQuery)
            rows = result.fetchall()
            table = []
            for row in rows:
                table.append(row)
            print("List of tables in the database " + database)
            print(tabulate(table, headers=["Table schema","Table name"], tablefmt="psql"), "\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            try:
                Connect()
                if database == "":
                    List()
                else:
                    List(database)
            except KeyboardInteerrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Database " + database + " does not exist on the server " + settings.global_config_array["server"] + ".\n")
        else:
            print("Error:",e.args[0],"\n",e,"\n")
    except Exception as e:
        print("Error:",e.args[0],"\n",e,"\n")   
        
def Import(table = "", fileName = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            while fileName == "" or not os.path.exists(filePath):
                fileName = str(input("Please insert the CSV filename for import: "))
                if fileName == "":
                    print("You did not enter the filename.\n")
                else:
                    filePath = "exports/" + fileName + ".csv"
                if os.path.exists(filePath):
                    print("File " + fileName + ".csv found.\n")
                else:
                    print("File " + fileName + ".csv not found.\n")
            with open(filePath, 'r') as file:
                dbConnection = settings.global_config_array["active_sql_connection"]
                reader = csv.reader(file)
                columns = next(reader)
                if table != "":
                    createTempTableQuery = "SELECT * INTO schema." + table + " FROM schema." + fileName + " WHERE 1 = 0"
                    cursor = dbConnection.cursor()
                    cursor.execute(createTempTableQuery)
                    cursor.commit()
                    print("Temporary table " + table + " has been created.\n")
                    query = "insert into " + table + "({0}) values ({1})"
                    cursor = dbConnection.cursor()
                    for r in reader:
                        cursor.execute(query, r)
                        cursor.commit()
                else:
                    query = "insert into " + fileName + "({0}) values ({1})"
                    query = query.format(','.join(columns), ','.join('?' * len(columns)))
                    cursor = dbConnection.cursor()
                    for r in reader:
                        cursor.execute(query, r)
                        cursor.commit()
                print("File " + fileName + " has been successfully imported to the destination table " + table)
                print("Import finished successfully.\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            try:
                Connect()
                if table != "" and fileName == "":
                    Import(tabl)
                elif table != "" and fileName != "":
                    Import(table, fileName)
                else:
                    Import()
            except KeyboardInterrupt:
                print("\nTerminating command...\n")        
    except KeyboardInterrupt:
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == "42S02":
            print("Error " + e.args[0] + ": Cannot create a temporal table - referenced object does not exist in the selected database.\n")
        else:
            print("Error",e.args[0] + ":\n",e,"\n")
            
def Drop(table = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            while table == "":
                table = str(input("Insert name of the table selected for drop: "))
                if table == "":
                    print("You did not enter the table name.\n")
            dbConnection = settings.global_config_array["active_sql_connection"]
            cursor = dbConnection.cursor()
            query = "drop table " + table
            cursor.execute(query)
            cursor.commit()
            print("Table " + table + " has been dropped successfully.\n")
        else:
            print("There is no active connection to the database. Redirecting to connect action...\n")
            try:
                Connect()
                if table != "":
                    Drop(table)
                else:
                    Drop()           
            except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        print("\nTerminating command...\n")
    except pyodbc.Error as e:
        print("Error " + e.args[0] + ":\n" + e + "\n")
    except Exception as e:
        print("Error " + e.args[0] + ":\n" + e + "\n")
        
def ConvertToXml(table = ""):
    try:
        if settings.global_config_array["active_sql_connection"] != None:
            if settings.global_config_array["table"] != None and table == "":
                table = settings.global_config_array["table"]
            elif settings.global_config_array["table"] == None and table == "":
                while table == "":    
                    table = str(input("Table name: "))
                    if table == "":
                        print("You did not enter table name.\n")
            dbConnection = settings.global_config_array["active_sql_connection"]
            cursor = dbConnection.cursor()
            selectQuery = list("select * from " + table)
            selectQuery = ''.join(selectQuery)
            columnsQuery = list("select column_name from information_schema.columns where table_name = '" + table + "'")
            columnsQuery = ''.join(columnsQuery)
            cols = cursor.execute(columnsQuery).fetchall()
            columns = list(str(c) for c in cols)
            columns = list([c.replace('(','').replace(')','').replace(' ','').replace("'",'').replace(',','').strip() for c in columns])
            rows = cursor.execute(selectQuery).fetchall()
            xmlPath = settings.global_config_array["xmlPath"]
            if os.path.exists(xmlPath):
                pass
            else:
                os.mkdir(xmlPath)
                print("/xml directory not found, creating...")
            fileName = table + ".xml"
            finalPath = os.path.join(path, xmlPath, fileName)
            indent_count = 1
            if os.path.exists(finalPath):
                print("File",fileName,"already exists. Do you want to overwrite it? [Y/n]", end='')
                confirmAction = str(input())
                if confirmAction == "Y" or confirmAction == "y":
                    with open(finalPath, "w+", newline='') as xmlFile:
                        xmlFile.write("<?xml version='1.0' ?>\n")
                        xmlFile.write("<%s>\n" % table)
                        for row in rows:
                            xmlFile.write("\t<field>\n")
                            indent_count += 1
                            for j in range(len(row)):
                                xmlFile.write("\t" * indent_count + "<%s>\n" % str(columns[j]))  # column headers
                                xmlFile.write("\t" * (indent_count + 1) + "%s\n" % str(row[j]))
                                xmlFile.write("\t" * indent_count)
                                xmlFile.write("</%s>\n" % str(columns[j]))  # column headers
                            indent_count = 1
                            xmlFile.write("\t</field>\n")
                        xmlFile.write("</%s>\n" % table)
                        print("SQL-XML conversion task finished successfully. File",fileName,"has been created.\n")
                        xmlFile.close()
                elif confirmAction == "N" or confirmAction == "n":
                    print("Aborting...\n")
            else:
                with open(finalPath, "w+", newline='') as xmlFile:
                        xmlFile.write("<?xml version='1.0' ?>\n")
                        xmlFile.write("<%s>\n" % table)
                        for row in rows:
                            xmlFile.write("\t<field>\n")
                            indent_count += 1
                            for j in range(len(row)):
                                xmlFile.write("\t" * indent_count + "<%s>\n" % str(columns[j]))  # column headers
                                xmlFile.write("\t" * (indent_count + 1) + "%s\n" % str(row[j]))
                                xmlFile.write("\t" * indent_count)
                                xmlFile.write("</%s>\n" % str(columns[j]))  # column headers
                            indent_count = 1
                            xmlFile.write("\t</field>\n")
                        xmlFile.write("</%s>\n" % table)
                        print("SQL-XML conversion task finished successfully. File",fileName,"has been created.\n")
                        xmlFile.close()
        else:
             print("There is no active connection to the database. Redirecting to connect action...\n")
             try:
                 Connect()
                 if table != "":
                     ConvertToXml(table)
                 else:
                     ConvertToXml()           
             except KeyboardInterrupt:
                print("\nTerminating command...\n")
    except KeyboardInterrupt:
        if dbConnection:
            dbConnection.close()
        dbConnection = None
        print("\nTerminating command...\n")
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
        
commands = {
    "exit": { "exec": Exit, "descr": "Exit the program" },
    "connect": { "exec": Connect, "descr": "<server> <database> - Open new connection to the target database" },
    "close": { "exec": Close, "descr": "Close active connection to the database" },
    "logout": { "exec": Logout, "descr": "Return to splash screen" },
    "xml": { "exec": ConvertToXml, "descr": "Exports target table into XML file" },
    "show": { "exec": Show, "descr": "<table> - List all rows in the selected table" },
    "add": { "exec": Add, "descr": "<table> <rowId> - Add new record to the selected table" },
    "delete": { "exec": Delete, "descr": "<table> <rowId> - Remove the existing record from the selected table" },
    "edit": { "exec": Edit, "descr": "<table> <rowId> - Modify the existing record in the selected table" },
    "import": { "exec": Import, "descr": "<destination_table> <file_name> - Import existing CSV file into the selected database" },
    "list": { "exec": List, "descr": "Display list of tables in the selected database" },
    "switch": { "exec": Switch, "descr": "<table> - If no new table name is provided, remove focus from the current table, otherwise switch to the another table." },
    "help": { "exec": Help, "descr": "Displays this commands' overview" },
    "export": { "exec": Export, "descr": "<table> - Exports currently selected table to .csv file" },
    "clear": { "exec": Clear, "descr": "This command clears the console window" },
    "drop": { "exec": Drop, "descr": "<table> - Drop the selected table" },
    "status": { "exec": Status, "descr": "Displays current session's data" },
    "query": { "exec": Query, "descr": "Run a specific query in the database" },
    "aliases": {
        "cls": { "exec": Clear, "descr": "This command clears the console window" },
        "exp": { "exec": Export, "descr": "Exports currently selected table to .csv file" },
        "quit": { "exec": Exit, "descr": "Exit the program" },
        "del": { "exec": Delete, "descr": "Remove the existing record from the selected table" }
    }
}
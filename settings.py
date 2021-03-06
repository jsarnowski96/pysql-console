# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 20:56:04 2019

@author: Jakub Sarnowski
"""

def init():
    global global_config_array
    global db_drivers

    db_drivers = {
        "MSSQL": "ODBC Driver 17 for SQL Server",
        "MySQL": "MySQL ODBC 3.51 Driver"
    }
    
    global_config_array = {
            "username": None,
            "password": None,
            "driver": db_drivers["MSSQL"],
            "database": None,
            "server": None,
            "table": None,
            "exportPath": "exports",
            "sourceCsvFile": None,
            "xmlPath": "xml",
            "user_sql_session": None,
            "active_sql_connection": None
    }

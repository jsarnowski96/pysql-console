# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 20:56:04 2019

@author: Jakub Sarnowski
"""

def init():
    global global_config_array
    global_config_array = {
            "username": None,
            "password": None,
            "database": None,
            "server": None,
            "table": None,
            "secure_sql_user_session": None,
            "active_sql_connection": None
    }
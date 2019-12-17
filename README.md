```
                         _____   __ __   __  _      ___ __  __  _   __   __  _   ___  
                        | _,\ `v' /' _/ /__\| | __ / _//__\|  \| |/' _/ /__\| | | __| 
                        | v_/`. .'`._`.| \/ | ||__| \_| \/ | | ' |`._`.| \/ | |_| _|  
                        |_|   !_! |___/ \_V_\___|  \__/\__/|_|\__||___/ \__/|___|___|
                                                                            v.0.2.15
```

# PySql-Console (under development)
Command line emulator written in Python 3.x

### Table of contents
[Introduction](#introduction)<br />
[Current features](#current-features)<br />
[Planned features](#planned-features)<br />
[File structure and dependant methods listing](#file-structure-and-dependant-methods-listing)<br />
[Requirements](#requirements)<br />
[List of available commands](#list-of-available-commands)<br />
[List of commands' aliases](#list-of-commands-aliases)<br />
[CLI's interactive mode](#clis-interactive-mode)<br />
[To do](#to-do)<br />
[Known issues](#known-issues)<br />
[Release notes](#release-notes)<br />

## Introduction
PySql-Console is a simple program emulating the command line interface, designed to interact with MS SQL environment. Due to Python's limitations related to internal command execution, some of the features introduced in this program are a sort of workarounds (for example user authentication system or multiple `input()` parameters treated as a separate strings kept in `list()` object). Thus the code might look a bit groggy and unsophisticated in some places, but during the development process I'm going to polish some things up.

PySql-Console allows user to interact with MS SQL database and its content. In future I'm going to implement other features like SQL-XML converter, text editor or even system-wide operations' support.<br /><br />

## Current features:
- create a connection with local or external MS SQL database
- display contents of the selected table (currently in raw, unformatted form)
- export selected table to .csv file
- implementation of user authentication mechanism based on Windows SQL Server Authentication
- executing commands directly or via aliases
<br />

## Planned features:
- full CRUD integration
- read data from .csv file and display it on the screen
- importing data from .csv file into the selected database/table
- SQL-XML converter and vice-versa
- integration with other database engines, such as MariaDB, MySQL, PostgreSQL etc.
- system-wide commands
<br />

## File structure and dependant methods listing:
- `pysqlconsole.py` - top layer py script handling user input and calling sub-routines from `commands.py`
  - `drawInitBoard()` - renders the program's logo screen<br />
  - `UserAuthentication()` - method responsible for performing user authentication. It keeps the main user identity connection opened during whole runtime<br />
  - `InputHandler()` - method processesing user input received from `MainActivity()` and executing calls to `commands.py` stored methods<br />
  - `MainaActivity()` - method responsible for acquiring user input and calling `InputHandler()` method<br />
  - `Startup()` - core `pysql-console` method invoking all dependant methods in a strict, predetermined order<br />
- `commands.py` - contains implementations of all internal commands used by the program<br />
  - `Exit()`<br />
  - `Connect()`<br />
  - `Close()`<br />
  - `Logout()`<br />
  - `Show()`<br />
  - `Query()`<br />
  - `Export()`<br />
  - `Clear()`<br />
  - `Status()`<br />
  - `Switch()`<br />
  - `Help()`<br />
- `settings.py` - global configuration file feeding requested data to both `pysqlconsole.py` and `commands.py`<br />

## Requirements:
- Python 3.x
- non standard-issue `pyodbc` and `tabulate` libraries
- configured account on local/remote MS SQL server with `SQL Server and Windows Authentication mode` enabled
- before you can use the program, you have to adjust server's name/IP and default database in `UserAuthentication()` method to your personal needs. Although using `master` as a default database might be sufficient, I highly recommend testing some of these settings beforehand. If you wish to connect with a certain server instance or you are using a non-standard port, you can use `Server=server_name\instance_name`<br />or `Server=server_name,port_number`, respectively. Use below template as a general reference point:
```
dbConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=;'
                              'Database=;'
                              'uid='+username+';'
                              'pwd='+password+';'
                              'Trusted_Connection=no;')  
```
<br />


## List of available commands:
```
exit: exits the program (eventually)
close: close the active MS SQL connection
connect <server> <database>: create an active connection to the target MS SQL database
show <table>: displays the content of the selected table
add <value 1> <value 2> ... <value n>: append new row to the selected table - in development
edit <row_id>: modify the specified row in the selected table - in development
query: allows for direct SQL select statement's execution
status: returns the current user's session data.
switch <table>: switches current focus to another table.
help: displays the list of available commands and aliases
delete <row_id>: delete the specified row ID in the selected table - in development
drop <table>|<database>: drop the target table or database (destructive) - in development
export <table>: exports the selected table to .csv file (otherwise prompt for table's name)
logout: releases pseudo user credentials and returns to login screen
```
<br />

## List of commands' aliases:
```
exp: export command alias
quit: exit command alias
del: delete command alias
```
<br />

## CLI's interactive mode:
Commands with implemented interactive mode allows user to provide the additional parameters "on the run" - in case of not providing any of the specified parameters or just a part of them. For example:
```
js $ export users
There is no connection established. Redirecting to connect action...

Server name: localhost
Database: test_db
Successfully connected to the localhost->test_db

js $ export users
users.csv export task finished successfully.

js $
```
Result:<br />
<img src="https://jsarnowski.pl/wp-content/uploads/2019/12/Przechwytywanie-1.png" /><br />

## To do:
- [ ] implementation of commands' functionalities:
  - [x] `close`
  - [ ] `add`
  - [ ] `delete`
  - [ ] `edit`
  - [ ] `drop`
  - [x] `status`
  - [x] `query`
  - [ ] `file <read>|<write> <file_name>`
  - [x] `help`
- [x] migration of `commands.py` method calls coming from `pysqlconsole.py` to the nested dictionaries binded with command's keys.<br />
- [ ] all SQL-related commands binded with one specific command as optional parameters<br />
(for example `sql connect`, `sql show`, `sql export`, `sql edit`, etc.)
- [x] fix bug in `Exit()` method
- [x] fix bug in `Export()` method
- [x] better format of table's listed content
<br />

## Known issues:
- ~~problem with exiting the app due to credential variables not being removed from the memory. Ctrl+c forced exit required.~~ <- <i>problem applied exclusively to Spyder environment and IPython console.</i>
- `pyodbc` library's limitations prevents some of the tables from being processed (throws `DataError` exception) - most likely caused by `datetime` type fields. The problem lies mostly in Microsoft's way of data types' implementation, so unfortunately there is no easy fix for it.<br />
- ~~export does its job only partially since it replicates a single row N times instead of processing next rows.~~ fixed
- ~~problem with using aliases~~ - fixed<br />
- problem with multiline cells' formatting which breaks whole table's view<br/>
- MS SQL Server throws error `23000` upon inserting a foreign key ID into the selected table. Implementation of `Add()` method postponed until further notice<br />

## Release notes:
- <b>13/12/2019 changelog:</b><br />
            - Initial commit + main script's upload<br />
            - Wrapping `UserAuthentication()` database connection sub-routine in try...except clause<br />
            - ASCII Logo tweaks<br />
- <b>14/12/2019 changelog:</b><br />
            - Fixed bug in `Exit()` method - script is now finishing properly<br />
            - ~~Introduced new bug in close proximity to `UserAuthentication()` and `InputLoop()` methods - first execution of any command leads to login screen. After inserting credentials for the second time, all commands seem to work correctly. Currently under investigation~~ - fixed<br />
            - Code refactoring in `MainActivity()` - removed redundant nested execution loop and wrapped internal code in try...except clause<br />
            - Better formatted table's content after `show` command's call. Still needs a bit of tinkering.<br />
            - Fixed the `UserAuthentication()`/`InputLoop()` bug causing user to land on login page after first command's execution.<br />
            - Refactored `UserAuthentication()` method - switched `pyodbc` driver to `ODBC Driver 17 for SQL Server` which allows for more reliable server-side user validation. The same driver change applies to all other methods establishing active connection with the database<br />
            - New `settings.py` global configuration file storing the globally-accessible DB connection data, user's active credentials, etc.<br />
- <b>15/12/2019 changelog:</b><br />
            - New exception handlers for `pyodbc.Error` returning codes `28000` and `42S02` for incorrect table/database name.<br />
            - New command `status` displaying content of `global_config_array`, including non-set key-value pairs.<br />
            - Visual adjustments of `status` output<br />
            - New command `switch` allows users to lift their focus off the currently selected table or move it to another table.<br />
            - `Export()` method: fix of issue related with file validation sub-routine.<br />
- <b>16/12/2019 changelog:</b><br />
            - Changes in exception handling mechanism - now it is more accurate, specific and covers a wider range of errors.<br />
            - Added new exception handle for error `08001` in case of connection failure to non-existing or not DNS-mapped SQL server.<br />
            - Major changes in `commands` dictionary - migrated method calls from `pysqlconsole.py` directly into nested command's dictionaries with `exec` key. Added new `query` command which allows for writing and executing a personalized SQL select statement. Command's fallback is similar to `export` or `show` commands - in case of no active DB connection, user is redirected to `Connect()` action.<br />
- <b>17/12/2019 changelog:</b><br />
            - Greatly improved table's output data format thanks to the application of `tabulate` library. Now tables' output is much more readable and organized.<br />
            - Change in specific commands' fallback behaviour - upon filling the missing data in `connect` action, user is redirected back to the initial command while all previously obtained optional parameters were stored for later use and are fully accessible.<br />
            - Added `KeyboardInterrupt` exception handle for `Delete()` method.<br />
            - Fixed bug in `Logout()` method related to `active_sql_session` field not being set to `None` upon method's callback.<br />

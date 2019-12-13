# bat-con (under development)
Command line emulator written in Python 3.x

### Table of contents
[Introduction](#introduction)<br />
[Current features](#current-features)<br />
[Planned features](#planned-features)<br />
[List of available commands](#list-of-available-commands)<br />
[List of commands' aliases](#list-of-commands-aliases)<br />
[Commands' interactive mode](#commands-interactive-mode)<br />
[To do](#to-do)<br />
[Known issues](#known-issues)<br />

## Introduction
Bat-con is a simple program emulating the command line interface. Due to Python's limitations, some of the features introduced by this program are sort of workarounds (for example user authentication system or multiple `input()` parameters treated as a separate strings kept in `list()` object). Thus the code might look a bit groggy and unsophisticated in some places, but during the development process I'm going to polish some things up.

Bat-con allows user to interact with MS SQL database and its content. In future I'm going to implement other functions such as SQL-XML converter, text editor or even system-wide operations' support.<br /><br />

## Current features:
- create a connection with local or external MS SQL database
- display contents of the selected table (currently in raw, unformatted form)
- export selected table to .csv file
- implementation of pseudo user authentication mechanism
- executing commands directly or via aliases
<br />

## Planned features:
- full CRUD integration
- importing data from .csv file into the selected database
- SQL-XML converter and vice-versa
- system-wide commands
<br />

## List of available commands:
```
exit: exits the program (eventually)
close: close the active MS SQL connection
connect <server> <database>: create an active connection to the target MS SQL database
show <table>: displays the content of the selected table
add <value 1> <value 2> ... <value n>: append new row to the selected table
edit <row_id>: modify the specified row in the selected table
delete <row_id>: delete the specified row ID in the selected table
drop <table>|<database>: drop the target table or database (destructive)
export <table>: exports the selected table to .csv file (otherwise prompt for table's name)
logout: releases pseudo user credentials and returns to login screen
```
<br />

## List of commands' aliases:
```
exp: export command alias
quit: exit command alias
```
<br />

## Command's interactive mode:
Commands allowing user to provide the additional parameters treats them only as optional - in case of not providing any of the specified parameters or just a part of them, these commands have implemented user interactive mode for providing the missing data required for performing their basic task and as a way of handling exceptions. For example:
```
js $ connect localhost
Database: test_db
Connection with localhost->test_db has been successfully established.
```
<br />

## To do:
- implementation of commands' functionalities:
  - close
  - add
  - delete
  - edit
  - drop
- fix the exit command's bug
- fix the export command's bug
- better format of table's listed content
<br />

## Known issues:
- problem with exiting the app due to credential variables not being removed from the memory. Ctrl+c forced exit required.
- `pyodbc` library's limitations prevents some of the tables from being processed (throws `DataError` exception) - most likely caused by boolean data type fields.
- export does its job only partially since it replicates a single row N times instead of processing next rows.


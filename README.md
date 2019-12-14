```
                +-----------------------------------------------------------------------------+
                |                     _..-'(                       )`-.._                     |
                |                  ./'. '||\\.       (\_/)       .//||` .`\.                  |
                |               ./'.|'.'||||\\|..    )O O(    ..|//||||`.`|.`\.               |
                |            ./'..|'.|| |||||\`````` '`"'` ''''''/||||| ||.`|..`\.            |
                |          ./'.||'.|||| ||||||||||||.     .|||||||||||| |||||.`||.`\.         |
                |         /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\         |
                |        '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`        |
                |       '.||| ||||||||| |/'   ``\||``     ''||/''   `\| ||||||||| |||.`       |
                |       |/' \./'     `\./         \!|\   /|!/         \./'     `\./ `\|       |
                |       V    V         V          }' `\ /' `{          V         V    V       |
                |       `    `         `               V               '         '    '       |
                +-----------------------------------------------------------------------------+
                                                                                    
    _/_/_/                _/                    _/_/_/                                          _/
   _/    _/    _/_/_/  _/_/_/_/              _/          _/_/    _/_/_/      _/_/_/    _/_/    _/    _/_/
  _/_/_/    _/    _/    _/      _/_/_/_/_/  _/        _/    _/  _/    _/  _/_/      _/    _/  _/  _/_/_/_/
 _/    _/  _/    _/    _/                  _/        _/    _/  _/    _/      _/_/  _/    _/  _/  _/
_/_/_/      _/_/_/      _/_/                _/_/_/    _/_/    _/    _/  _/_/_/      _/_/    _/    _/_/_/
```

# Bat-Console (under development)
Command line emulator written in Python 3.x

### Table of contents
[Introduction](#introduction)<br />
[Current features](#current-features)<br />
[Planned features](#planned-features)<br />
[File structure](#file-structure)<br />
[List of available commands](#list-of-available-commands)<br />
[List of commands' aliases](#list-of-commands-aliases)<br />
[CLI's interactive mode](#clis-interactive-mode)<br />
[To do](#to-do)<br />
[Known issues](#known-issues)<br />
[Release dates](#release-dates)<br />

## Introduction
Bat-Console is a simple program emulating the command line interface, designed to interact mostly with MS SQL environment. Due to Python's limitations related to internal command execution, some of the features introduced by this program are sort of workarounds (for example user authentication system or multiple `input()` parameters treated as a separate strings kept in `list()` object). Thus the code might look a bit groggy and unsophisticated in some places, but during the development process I'm going to polish some things up.

Bat-Console allows user to interact with MS SQL database and its content. In future I'm going to implement other features like SQL-XML converter, text editor or even system-wide operations' support.<br /><br />

## Current features:
- create a connection with local or external MS SQL database
- display contents of the selected table (currently in raw, unformatted form)
- export selected table to .csv file
- implementation of pseudo user authentication mechanism
- executing commands directly or via aliases
<br />

## Planned features:
- full CRUD integration
- read data from .csv file and display it on the screen
- importing data from .csv file into the selected database
- SQL-XML converter and vice-versa
- system-wide commands
<br />

## File structure:
- `batconsole.py` - top layer py script handling user input and calling sub-routines from `commands.py`
  - `commands.py` - contains implementations of all internal commands used by the program
- `settings.py` - global configuration file feeding requested data to both `batconsole.py` and `commands.py`
<br />

## List of available commands:
```
exit: exits the program (eventually)
close: close the active MS SQL connection
connect <server> <database>: create an active connection to the target MS SQL database
show <table>: displays the content of the selected table
add <value 1> <value 2> ... <value n>: append new row to the selected table - in development
edit <row_id>: modify the specified row in the selected table - in development
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
```
<br />

## CLI's interactive mode:
Commands with implemented interactive mode allows user to provide the additional parameters "on the run" - in case of not providing any of the specified parameters or just a part of them. For example:
```
js $ connect localhost
Database: test_db
Connection with localhost->test_db has been successfully established.
```
<br />

## To do:
- [ ] implementation of commands' functionalities:
  - [x] `close`
  - [ ] `add`
  - [ ] `delete`
  - [ ] `edit`
  - [ ] `drop`
  - [ ] `file <read>|<write> <file_name>`
  - [x] `help`
- [x] fix bug in `Exit()` method
- [ ] fix bug in `Export()` method
- [x] better format of table's listed content
<br />

## Known issues:
- ~~problem with exiting the app due to credential variables not being removed from the memory. Ctrl+c forced exit required.~~
- `pyodbc` library's limitations prevents some of the tables from being processed (throws `DataError` exception) - most likely caused by boolean data type fields.
- export does its job only partially since it replicates a single row N times instead of processing next rows.

## Release notes:
- 13/12/2019 summary:<br />
            - Initial commit + main script's upload<br />
            - Wrapping UserAuthentication() db connection sub-routine in try...except clause<br />
            - ASCII Logo tweaks<br />
- 14/12/2019 summary:<br />
            - Fixed bug in `Exit()` method - script is now finishing properly<br />
            - Introduced new bug in close proximity to `UserAuthentication()` and `InputLoop()` methods - first execution of any command leads to login screen. After inserting credentials for the second time, all commands seem to work correctly. Currently under investigation.<br />
            - Code refactoring in `MainActivity()` - removed redundant nested execution loop and wrapped internal code in try...except clause<br />
            - Better formatted table's content after `show` command's call.<br />
            - Fixed the `UserAuthentication()`/`InputLoop()` bug causing user to land on login page after first command's insertion.<br />
            - Refactored user authentication method - switched `pyodbc` driver to `ODBC Driver 17 for SQL Server` which allowed for reliable server-side user validation.<br />
            - New `settings.py` global configuration file storing the globally-accessible DB connection data, user's active credentials, etc.<br />


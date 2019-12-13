# bat-con
Command line emulator written in Python 3.x

# Current functionalities:
- create a connection with local or external MS SQL database
- display contents of the selected table
- export selected table to .csv file
- implementation of pseudo user authentication mechanism based on Users or AuthUsers tables (depending on the config)
- executing commands directly or via aliases

# List of available commands:
```
exit: exits the program (eventually)
close: close the active MS SQL connection
connect <server> <database>: create an active connection to the target MS SQL database
show <table>: displays the content of the selected table
add <value 1> <value 2> ... <value n>: append new row to the selected table
edit <row_id>: modify the specified row in the selected table
delete <row_id>: delete the specified row ID in the selected table
drop <table>|<database> (destructive): drop the target table or database
export <table>: exports the selected table to .csv file (otherwise prompt for table's name)
logout: releases pseudo user credentials and returns to login screen
```
# List of commands' aliases:
```
exp: export command alias
quit: exit command alias
```

# To do:
- implementation of commands' functionalities:
  - close
  - add
  - delete
  - edit
  - drop
- fix the exit command's bug
- fix the export command's bug

# Known issues:
- problem with exiting the app due to credential variables not being removed from the memory. Ctrl+c forced exit required.
- pyodbc library's limitations preventing some of the tables from being processed (throws DataError exception), most likely caused by boolean data type fields.
- export does its job only partially since it replicates a single row N times instead of processing next rows.


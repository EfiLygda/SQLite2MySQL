# SQLite2MySQL

Simple command line converter of SQLite database file directly to MySQL database.

# Requirements
```
python==3.8.18
numpy==1.26.4
pandas==2.3.0
```

# Usage

**Step 1:** Download the Python script `SQLite2MySQL.py'.

**Step 2:** Navigate to the directory of the script through the command line (i.e. using `cd`).

**Step 3:** For Windows users, in order the make the new MySQL database and add the tables from the SQLite database file, run the command as:
```
> py SQLite2MySQL.py -sqlite database.sqlite -u user -pwd password -host hostname -db New_MySQL_database_name
```

In case of exporting the original database to csv files use the flag -csv, as below: 
```
> py SQLite2MySQL.py -sqlite database.sqlite -u user -pwd password -host hostname -db New_MySQL_database_name -csv
```
and the files will be exported to a new directory called 'csv' in the directory from which the command is run from.


In case of another output directory argument -o can be used as below:
```
> py SQLite2MySQL.py -sqlite database.sqlite -u user -pwd password -host hostname -db New_MySQL_database_name -csv -o csv_output_directory
```

# Help

```
usage: SQLite2MySQL.py [-h] --sqlite_filename SQLITE_FILENAME --username USERNAME --password PASSWORD --host HOST
                       --database DATABASE [--csv] [--out_dir OUT_DIR]

options:
  -h, --help            show this help message and exit
  --sqlite_filename SQLITE_FILENAME, -sqlite SQLITE_FILENAME
                        (str) Old SQLite Database Path
  --username USERNAME, -u USERNAME
                        (str) MySQL Username
  --password PASSWORD, -pwd PASSWORD
                        (str) MySQL password
  --host HOST, -host HOST
                        (str) MySQL host name.
  --database DATABASE, -db DATABASE
                        (str) MySQL new database name.
  --csv, -csv           Whether to export the database tables to csv. OFF: (default) no csv files are exported, ON:
                        csv files will be exported
  --out_dir OUT_DIR, -o OUT_DIR
                        (str) Where to export the database tables to csv. When -csv is not ON but -o is given nothing
                        is exported.
```

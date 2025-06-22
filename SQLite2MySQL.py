import os
import argparse
import sqlite3
from sqlalchemy import create_engine
import pandas as pd


# ----------------------------------------------------------------------------------------------------------------------
# Building Command
# ----------------------------------------------------------------------------------------------------------------------

# --- Defining the argument parser for the command ---
parser = argparse.ArgumentParser()

# --- Required arguments of the command ---
# SQLite database absolute file name
parser.add_argument('--sqlite_filename', '-sqlite',
                    help='(str) Old SQLite Database Path',
                    type=str,
                    required=True)

# MySQL username
parser.add_argument('--username', '-u',
                    help='(str) MySQL Username',
                    type=str,
                    required=True)

# MySQL password
parser.add_argument('--password', '-pwd',
                    help='(str) MySQL password',
                    type=str,
                    required=True)

# MySQL host name
parser.add_argument('--host', '-host',
                    help='(str) MySQL host name.',
                    type=str,
                    required=True)

# MySQL new database name
parser.add_argument('--database', '-db',
                    help='(str) MySQL new database name.',
                    type=str,
                    required=True)

# --- Optional arguments for converting database to csv ---
# When on database will be exported as csv files will be exported
parser.add_argument('--csv', '-csv',
                    help='''Whether to export the database tables to csv.
                    OFF: (default) no csv files are exported, ON: csv files will be exported''',
                    default=0,
                    action="store_true")

# Optional output directory for the csv files of the database.
# If -csv is ON but -o is none then default is root directory
parser.add_argument('--out_dir', '-o',
                    help='''(str) Where to export the database tables to csv.
                    When -csv is not ON but -o is given nothing is exported.''',
                    type=str)

# --- Parse arguments to extract user inputs ---
args = parser.parse_args()


# ----------------------------------------------------------------------------------------------------------------------
# Preparing User Inputs for Command
# ----------------------------------------------------------------------------------------------------------------------

# --- Extract user inputs to variables ---
sqlite_filename = args.sqlite_filename
username = args.username
password = args.password
host = args.host
database = args.database
csv = [True if args.csv else False][0]

# --- Check if csv flag is ON and make the output csv directory ---
if csv:
    # Check if an output directory was given
    if args.out_dir:

        # Check if the output directory exists, and if not raise error
        if not os.path.exists(args.out_dir):
            raise RuntimeError(f'Output csv directory "{args.out_dir}" does not exist!')

        # If it exists output dir will be in a new directory
        CSV_DIR = os.path.join(args.out_dir, 'csv')

    else:
        # If the output directory was not given but csv flag is ON then default output directory is root
        CSV_DIR = os.path.join('./', 'csv')

    # Make new csv folder if it does not exist
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)


# ----------------------------------------------------------------------------------------------------------------------
# Converting SQLite tables to MySQL
# ----------------------------------------------------------------------------------------------------------------------

# --- Extracting SQLite tables ---

# Connecting to SQLite database file
con = sqlite3.connect(sqlite_filename)

# Defining cursor for the connection
cur = con.cursor()

# Extracting all available table names in database
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Connecting to MySQL
mysql_engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

# For each table in original SQLite database, add it to MySQL database directly
# Optional: Extract csv file for each available table
for table in tables:

    # Extract table name
    table_name = table[0]

    # Read a table into a pandas DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)

    # Add table to MySQL database through DataFrame
    df.to_sql(table_name, mysql_engine, if_exists='replace', index=False)

    # Print success message
    print(f"Created table {table_name} in {database}.")

    # If csv flag is ON then extract table to csv
    if csv:
        out_path = os.path.join(CSV_DIR, f'{table_name}.csv')
        df.to_csv(out_path, index=False, na_rep='NULL')

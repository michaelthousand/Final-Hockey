import sqlite3
from pathlib import Path

# Function for creating a database if it doesn't already exist
def add_db(file_name):
    path = Path('save files/' + file_name +'.db')
    if path.is_file():
        print('File already exists')
        #return # Add some indication that there is already a file with the db name
    else:
        conn = sqlite3.connect('save files/' + file_name + '.db')
        conn.commit()
        conn.close()

# Function for creating roster tables in that database
def add_roster_table(file_name, year):
    path = Path('save files/' + file_name + '.db')
    if path.is_file():
        table_name = 'roster_' + year
        conn = sqlite3.connect('save files/' + file_name + '.db')
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT NOT NULL,
                  last_name TEXT NOT NULL,
                  number TEXT NOT NULL,
                  position TEXT NOT NULL
                  );''')
        conn.commit()
        conn.close()
    else:
        print('The file does not exist')
        #return # Add some indication that there isn't a file with the db name

# Function for adding players to the roster database
def add_player(file_name, first_name, last_name, number, position, year):
    table_name = 'roster_' + year
    conn = sqlite3.connect('save files/' + file_name + '.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {table_name} (first_name, last_name, number, position) VALUES (?, ?, ?, ?)", (first_name, last_name, number, position))
    conn.commit()
    conn.close()

# DELETE AFTER TESTING - View all entries in a given database
def view_all(file_name, year):
    table_name = 'roster_' + year
    conn = sqlite3.connect('save files/' + file_name + '.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    return rows


#view_all('test', '2022_23')
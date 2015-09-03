import sqlite3

sqlite_file = 'the_great_db.sqlite'
table1 = 'house001'
field1 = 'unit_name'
field2 = 'datetime'
field3 = 'value'
t = 'table'


def setup_db():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?', (t, table1))
    if c.fetchone():
        print('Found a local database, setting it up for further use...')
    else:
        print('No database exists, creating a new one...')
        c.execute('CREATE TABLE {tn} ({fn1} {ft1}, '
                  '{fn2} DATETIME DEFAULT CURRENT_TIMESTAMP, '
                  '{fn3} {ft3})'
                  .format(tn=table1, fn1=field1, ft1='TEXT', fn2=field2, fn3=field3, ft3='INTEGER'))
        conn.commit()
    conn.close()


def open_and_store(data):
    conn, c = connect()
    c.execute('INSERT INTO {tn} ({fn1}, {fn3}) VALUES ("house001", ?)'
              .format(tn=table1, fn1=field1, fn3=field3), (data,))
    close(conn)


def connect():
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c


def close(conn):
    """ Commit changes and close connection to the database """
    conn.commit()
    conn.close()

'''

# Prints Information of a SQLite database.

# E.g.,
#
"""
Total rows: 1
Column Info:
ID, Name, Type, NotNull, DefaultVal, PrimaryKey
(0, 'id', 'TEXT', 0, None, 1)
(1, 'date', '', 0, None, 0)
(2, 'time', '', 0, None, 0)
(3, 'date_time', '', 0, None, 0)
Number of entries per column:
date: 1
date_time: 1
id: 1
time: 1
"""

import sqlite3

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def close(conn):
    """ Commit changes and close connection to the database """
    #conn.commit()
    conn.close()

def total_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    c.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = c.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def table_col_info(cursor, table_name, print_out=False):
    """
       Returns a list of tuples with column information:
      (id, name, type, notnull, default_value, primary_key)

    """
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()

    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info

def values_in_col(cursor, table_name, print_out=True):
    """ Returns a dictionary with columns as keys and the number of not-null
        entries as associated values.
    """
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        c.execute('SELECT ({0}) FROM {1} WHERE {0} IS NOT NULL'.format(col, table_name))
        # In my case this approach resulted in a better performance than using COUNT
        number_rows = len(c.fetchall())
        col_dict[col] = number_rows
    if print_out:
        print("\nNumber of entries per column:")
        for i in col_dict.items():
            print('{}: {}'.format(i[0], i[1]))
    return col_dict


if __name__ == '__main__':

    sqlite_file = 'my_first_db.sqlite'
    table_name = 'my_table_3'

    conn, c = connect(sqlite_file)
    total_rows(c, table_name, print_out=True)
    table_col_info(c, table_name, print_out=True)
    values_in_col(c, table_name, print_out=True) # slow on large data bases

    close(conn)
'''
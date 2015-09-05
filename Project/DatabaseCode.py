import sqlite3

sqlite_file = 'the_great_db.sqlite'
table1 = 'house001'
field1 = 'unit_name'
field2 = 'datetime'
field3 = 'value'
t = 'table'


def setup_db():
    """ Create a database if one does not exist, as [unit_name, datetime, value]. """
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
    """ Open a connection to the db and store the provided data. """
    conn, c = connect()
    c.execute('INSERT INTO {tn} ({fn1}, {fn3}) VALUES ("house001", ?)'
              .format(tn=table1, fn1=field1, fn3=field3), (data,))
    close(conn)


# TODO: Build open_and_fetch
def open_and_fetch(arg):
    return arg


# TODO: As well as a way to run more custom queries...
def execute(query):
    return query


def connect():
    """ Make connection to an SQLite database file. """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c


def close(conn):
    """ Commit changes and close connection to the database. """
    conn.commit()
    conn.close()

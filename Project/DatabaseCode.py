import sqlite3

sqlite_file = 'the_great_db.sqlite'
table1 = 'house001'
field1 = 'datetime'
field2 = 'unit_id'
field3 = 'manufacturer'
field4 = 'type'
field5 = 'medium'
field6 = 'value'
field7 = 'unit'
t = 'table'


def setup_db():
    """ Create a database if one does not exist, as [unit_name, datetime, value]. """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?', (t, table1))
    if c.fetchone():
        print('Found a local database, setting it up for further use...')
    else:
        # Databasens struktur: datetime, ID(sec addr), Manufacturer, type(insta val),
        # medium(water), value(2598), unit(1L)
        print('No database exists, creating a new one...')
        c.execute('CREATE TABLE {tn} ('
                  '{fn1} DATETIME DEFAULT CURRENT_TIMESTAMP, '
                  '{fn2} TEXT, '
                  '{fn3} TEXT, '
                  '{fn4} TEXT, '
                  '{fn5} TEXT, '
                  '{fn6} TEXT, '
                  '{fn7} TEXT  '
                  ')'
                  .format(tn=table1,
                          fn1=field1,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7))
        conn.commit()
    conn.close()


def open_and_store(m):
    """ Open a connection to the db and store the provided mbus telegram. """

    conn, c = connect()
    # Databasens struktur: DATETIME, ID(sec_addr), MF, type(instant_val), Medium(water), Value(2598), Unit(1L)
    # En post per datablock i telegrammet!
    for b in m.data_blocks:
        c.execute('INSERT INTO {tn} ('  # Insert into table 'house1'
                  # '{fn1}, '  # datetime -- UNNECESSARY, GETS DEFAULT VALUE
                  '{fn2}, '  # unit_id
                  '{fn3}, '  # manufacturer
                  '{fn4}, '  # type
                  '{fn5}, '  # medium
                  '{fn6}, '  # value
                  '{fn7}) '  # unit
                  'VALUES (?, ?, ?, ?, ?, ?)'
                  .format(tn=table1,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7
                          ),
                  (
                      m.fields['id'],       # Unit ID
                      m.fields['mf'],       # Manufacturer
                      b[1]+' '+b[2],        # Type, e.g. "Instantaneous value"
                      m.fields['medium'],   # Medium
                      b[3],                 # Value
                      b[4],                 # Unit
                  ))
    close(conn)


# TODO: Build open_and_fetch
def open_and_fetch(arg):
    return arg


# TODO: As well as a way to run more custom queries. Where do I put the code that translates user input into SQL?
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

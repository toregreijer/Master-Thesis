import sqlite3

sqlite_file = 'the_great_db.sqlite'
field1 = 'datetime'
field2 = 'unit_id'
field3 = 'function'
field4 = 'description'
field5 = 'medium'
field6 = 'value'
field7 = 'unit'
field8 = 'manufacturer'
t = 'table'


def setup_db():
    """ Create a database if one does not exist, as [unit_name, datetime, value]. """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM sqlite_master WHERE type="table"')
    if c.fetchone():
        print('Found a local database, setting it up for further use...')
    else:
        # Databasens struktur: datetime, ID(sec addr), Manufacturer, type(insta val),
        # medium(water), value(2598), unit(1L)
        print('No database exists, creating a new one...')
        """
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
                          fn7=field7))  """
        conn.commit()
    conn.close()


def open_and_store(m):
    """ Open a connection to the db and store the provided mbus telegram. """
    unit_id = m.fields['id']
    tables = []
    conn, c = connect()
    c.execute('SELECT name FROM sqlite_master WHERE type="table"')
    for item in c.fetchall():
        tables.append(item[0])
    if unit_id in tables:
        print('Table {} exists, nothing new required.'.format(unit_id))
    else:
        print('Table {} does not exist, creating new table.'.format(unit_id))
        c.execute('CREATE TABLE {tn!r} ('
                  '{fn1} DATETIME DEFAULT CURRENT_TIMESTAMP, '
                  '{fn2} TEXT, '
                  '{fn3} TEXT, '
                  '{fn4} TEXT, '
                  '{fn5} TEXT, '
                  '{fn6} TEXT, '
                  '{fn7} TEXT, '
                  '{fn8} TEXT  '
                  ')'
                  .format(tn=unit_id,
                          fn1=field1,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7,
                          fn8=field8))
    # Databasens struktur:
    # field1 = 'datetime'
    # field2 = 'unit_id'
    # field3 = 'function'
    # field4 = 'description'
    # field5 = 'medium'
    # field6 = 'value'
    # field7 = 'unit'
    # field8 = 'manufacturer'
    # En post per datablock i telegrammet!
    for b in m.data_blocks:
        c.execute('INSERT INTO {tn!r} ('  # Insert into table 'unit_id'
                  '{fn2}, '
                  '{fn3}, '
                  '{fn4}, '
                  '{fn5}, '
                  '{fn6}, '
                  '{fn7}, '
                  '{fn8}) '
                  'VALUES (?, ?, ?, ?, ?, ?, ?)'
                  .format(tn=unit_id,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7,
                          fn8=field8
                          ),
                  (
                      m.fields['id'],       # Unit ID
                      b[1],                 # Function
                      b[2],                 # Description
                      m.fields['medium'],   # Medium
                      b[3],                 # Value
                      b[4],                 # Unit
                      m.fields['mf'],       # Manufacturer
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
